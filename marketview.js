function log(msg){
    console.log(arguments);
    if('string' === typeof msg) $('#log').prepend($('<div>').html(msg));
};

function jsonp(method, data, callback){
    $.ajax({
        url: method + '.jsonp',
        dataType: 'jsonp',
        type: 'GET',
        data: data,
        success:function(data){
            if(null !== data && 'string' === typeof data.error) log(data.error, arguments);
            callback(data);
        },
        error:function(){
            log('Unable to retrieve ' + method, arguments);
        }
    });
};

var colors = {
    'obc:1737d32b3bfdd06a177435a00e4ddd8befe804daece3cfa19508f1ec7a2df2a9:0:241614': 'red',
    'obc:f9931ace552776defae1114f551cfb09a6453f13956e042e8d78a8fd42af804b:0:241616': 'blue',
    'obc:b2e2fe91385b66b413d23d00c45d2958c273ba6248c2a5da0d3738ccffef74e9:0:242505': 'GLD',
    'obc:ebf6742cd705bfd3dbfb6470dadbf248a6cf90f4b54775ad54ce79ed45bd6365:0:242505': 'SLV'
};

var pairs = [];
function getpair(colordef1, colordef2){
    var pair = false;

    // Return pair if it exists
    $.each(pairs, function(idx, curpair){
        if(
            $.inArray(colordef1, curpair.colordefs) >= 0 &&
            $.inArray(colordef2, curpair.colordefs) >= 0
        ){
            pair = curpair;
            return false;
        }
    });
    if(false !== pair){
        return pair;
    }

    // or create a new one.
    pair = pairskelaton.clone().extend({
        'colordefs': [colordef1, colordef2]
    }).find('h2').html(
        (colors[colordef1] || 'unrecognized') + ' vs. ' + (colors[colordef2] || 'unrecognized')
    ).end();
    pairs.push(pair);
    pair.find('table').tablesorter();
    market.append(pair)
    return pair
}

function time(){
    var d = new Date();
    return $.map([d.getHours(), d.getMinutes(), d.getSeconds()], function(c){
        return (c < 10 ? '0' : '') + c;
    }).join(':');
}

function showproposal(proposal){
    var pair = getpair(proposal.give.colordef, proposal.take.colordef);
    var table;
    var price;
    if(proposal.give.colordef === pair.colordefs[0]){
        table = 'a';
        price = proposal.give.quantity / proposal.take.quantity;
    }else{
        table = 'b';
        price = proposal.take.quantity / proposal.give.quantity;
    }
    pair.find('table.proposals' + table).find('tbody').append($('<tr>').append(
        $('<td>').text(time()),
        $('<td>').text(proposal.give.quantity),
        $('<td>').text(price),
        $('<td>').text('none')
    )).end().trigger('update').trigger('sorton', [[[2, 0]]]).
    find('thead tr th').eq(2).click();
}

function getmessages(){
    jsonp('receive', {}, function(messages){
        $.each(messages, function(i, message){
            if('proposal' === message.subject && -1 === message.body.scheme){
                showproposal(message.body);
            }else if('fulfil' === message.body){
                ;
            }else if('confirm' == message.body){
                ;
            }
        });
        setTimeout('getmessages()', 1000);
    });
}

var market;
var pairskelaton;
$(function(){
    $('#nojs').remove();
    market = $('#market');
    pairskelaton = $('.pair').remove().show();

    $('input.colordef').replaceWith(
        $('<select>').addClass('colordef').append(
            $.map(colors, function(moniker, colordef){
                return $('<option>').val(colordef).text(moniker);
            })
        ).append(
            $('<option value="" disabled="disabled" selected="selected">select a color</option>')
        )
    );

    $('#sendproposal').click(function(e){
        var form = $(this).parent();
        var give = form.find('div.give');
        var take = form.find('div.take');
        var proposal = JSON.stringify({
            'scheme': -1,
            'version': -1,
            'give':{
                'colordef': give.find('select.colordef').val(),
                'quantity': give.find('input.quantity').val(),
                'utxos': $.parseJSON(give.find('textarea.utxos').val()),
            },
            'take':{
                'colordef': take.find('select.colordef').val(),
                'quantity': take.find('input.quantity').val(),
                'address': take.find('input.address').val(),
            }
        });
        jsonp(
            'send',
            {'subject': 'proposal', 'body': proposal},
            function(msgid){
                log('sending proposal in msg ' + msgid, msgid, proposal);
            }
        )
    });
    getmessages();
});
