// Formatted time.
function time(){
    var d = new Date();
    return $.map([d.getHours(), d.getMinutes(), d.getSeconds()], function(c){
        return (c < 10 ? '0' : '') + c;
    }).join(':');
}

// Log arguments to console, show first argumentst if it's a string.
function log(msg){
    console.log(arguments);
    if('string' === typeof msg) $('#log').prepend($('<div>').html(time() + ' ' + msg));
}

// JSONp request with data and callback
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
}

// Simple tx watcher with callback.
function watchfortx(txid, callback){
    $.ajax({
        url: 'https://testnet.helloblock.io/v1/transactions/' + txid,
        dataType: 'html',
        type: 'GET',
        success:function(data){
            callback(data);
        },
        error:function(){
            setTimeout(function(){watchfortx(arguments);}, 1000 * 60);
        }
    });
}

// Colors we know about. TODO These should be in an ini file or something.
var colors = {
    'obc:e738ac54b03a4f159e1412456bfb6b712e6c0730a73962d8e8fbcace07e8b031:0:260522': 'GLD',
    'obc:ee8c695734be4971a99e8f036c2ae6c10a5696cbe39646f9739cca39d1c63e7d:0:260524': 'SLV'
};

// Replace given elements with a dropdown selection of colors.
function colorchoice(elements){
    elements.replaceWith(
        $('<select>').addClass('colordef').append(
            $.map(colors, function(moniker, colordef){
                return $('<option>').val(colordef).text(moniker);
            })
        ).append(
            $('<option value="" disabled="disabled" selected="selected">select a color</option>')
        )
    );
}

// The market is divided into asset pairs.
var pairs = [];
// Return a pair if it exists, create a new one if it doesn't.
function getpair(colordef1, colordef2){
    var returnpair = false;

    // Return existing pair
    $.each(pairs, function(idx, curpair){
        if(
            $.inArray(colordef1, curpair.colordefs) >= 0 &&
            $.inArray(colordef2, curpair.colordefs) >= 0
        ){
            returnpair = curpair;
            return false;
        }
    });
    if(false !== returnpair){
        return returnpair;
    }

    // or create a new one and return it.
    returnpair = pairskelaton.clone().extend({
        'colordefs': [colordef1, colordef2]
    }).find('h1').html(
        (colors[colordef1] || 'unrecognized') + ' vs. ' + (colors[colordef2] || 'unrecognized')
    ).end();
    marketdiv.append(returnpair);
    returnpair.find('table').tablesorter();
    returnpair.graph = new Dygraph(
        returnpair.find('.graph').get(0),
        'Time, Price a->b, Price b->a' + "\n" +
        {
            'drawPoints': true,
            'showRoller': true
        }
    );
    // FIXME
    returnpair.graph.updateOptions({'file':
        'Time, Price a->b, Price b->a' + "\n" +
        '0,1,10' + "\n" +
        '1,2,7' + "\n" +
        '2,4,6'
    });
    pairs.push(returnpair);
    return returnpair
}

// Each proposal is a row in one of the conversion tables in its pair.
var proposals = {};
// Display a new proposal in the right table and catalogue it.
function showproposal(proposal){
    var hash = $.sha256(JSON.stringify(proposal));
    var pair = getpair(proposal.give.colordef, proposal.take.colordef);
    var table;
    var row;
    var price;

    // Catalogue row for future use.
    proposals[hash] = proposal;

    if(proposal.give.colordef === pair.colordefs[0]){
        price = proposal.give.quantity / proposal.take.quantity;
        table = 'a';
    }else{
        price = proposal.take.quantity / proposal.give.quantity;
        table = 'b';
    }

    row = $('<tr>').append(
        $('<td>').text(time()),
        $('<td>').text(proposal.give.quantity),
        $('<td>').text(price),
        $('<td>').text('none')
    );
    proposals[hash]['row'] = row;

    // Add proposal hash to the fulfil form.
    $('select.proposalhash').append(
        $('<option>').val(hash).text(
            proposal.give.quantity +
            colors[proposal.give.colordef] +
            ' for ' +
            proposal.take.quantity +
            colors[proposal.take.colordef]
        )
    );

    // Append the row and refresh the table.
    pair.find('table.proposals' + table).find('tbody').append(row).end().
    trigger('update').trigger('sorton', [[[2, 0]]]).
    find('thead tr th').eq(2).click();
}

// Replace the proposal hash input with a dropdown selection of proposals.
function proposalchoice(){
    $('input.proposalhash').replaceWith(
        $('<select>').addClass('proposalhash').append(
            '<option value="" disabled="disabled" selected="selected">select a proposal</option>'
        // Update form when proposal is selected.
        ).change(function(e){
            var select = $(e.target);
            var proposal = proposals[select.val()];
            var form = select.parent();
            var give = form.find('div.give');
            var take = form.find('div.take');
            give.find('select.colordef').val(proposal['take']['colordef']);
            give.find('input.quantity').val(proposal['take']['quantity']);
            take.find('select.colordef').val(proposal['give']['colordef']);
            take.find('input.quantity').val(proposal['give']['quantity']);
        })
    );
}

var fulfils = {};
// Color fulfilled proposal in red and add fulfil to accept list.
function showfulfil(fulfil){
    var hash = $.sha256(JSON.stringify(fulfil));
    var proposal = proposals[fulfil.proposalhash];

    // Catalogue row for future use.
    fulfils[hash] = fulfil;

    proposal.row.css('background-color', '#FF9999');

    // Add fulfil hash to the accept form.
    $('select.fulfilhash').append(
        $('<option>').val(hash).text(
            proposal.give.quantity +
            colors[proposal.give.colordef] +
            ' for ' +
            proposal.take.quantity +
            colors[proposal.take.colordef]
        )
    );
}

// Replace the fulfil hash input with a dropdown selection of fulfils.
function fulfilchoice(){
    $('input.fulfilhash').replaceWith(
        $('<select>').addClass('fulfilhash').append(
            '<option value="" disabled="disabled" selected="selected">select a fulfil</option>'
        // Update form when fulfil is selected.
        ).change(function(e){
            var select = $(e.target);
            var fulfil = fulfils[select.val()];
            var proposal = proposals[fulfil.proposalhash];
            var form = select.parent();
            var give = form.find('div.give');
            var take = form.find('div.take');
            give.find('select.colordef').val(proposal['give']['colordef']);
            give.find('input.quantity').val(proposal['give']['quantity']);
            give.find('textarea.utxos').val(JSON.stringify(proposal['give']['utxos']));
            take.find('select.colordef').val(proposal['take']['colordef']);
            take.find('input.quantity').val(proposal['take']['quantity']);
            take.find('input.address').val(proposal['take']['address']);
        })
    );
}

// Show an acceptance.
function showaccept(accept){
    var fulfil = fulfils[accept.fulfilhash];
    var proposal = proposals[fulfil.proposalhash];
    $('select.fulfilhash').find(
        'option[value="' + accept.fulfilhash + '"]'
    ).remove();
    $('select.proposalhash').find(
        'option[value="' + fulfil.proposalhash + '"]'
    ).remove();
    proposal.row.css('background-color', '#99FF99');
    watchfortx(accept.txid, function(){
        proposal.row.remove();
        log(
            'OMG, <a href="https://test.helloblock.io/transactions/' +
            accept.txid +
            '">look at that</a>'
        );
    });
}

// Get messages from queue.
function getmessages(){
    jsonp('receive', {}, function(messages){
        $.each(messages, function(i, message){
            if('proposal' === message.subject && -1 === message.body.scheme){
                showproposal(message.body);
            }else if('fulfil' === message.subject){
                showfulfil(message.body);
            }else if('accept' == message.subject){
                showaccept(message.body);
            }
        });
        //setTimeout('getmessages()', 1000);
    });
}

// Sends a proposal.
function sendproposal(form){
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
            log('sending proposal in msg ' + msgid, proposal);
        }
    );
}

// Helper function to turn a bitcoind flavored JSON TXO to ngccc tuple.
// The double square brackets prevent jquery's map from flattening the array.
function txobj2tuple(txo){return [[txo.txid, txo.vout]];}

// Sends a fulfil.
function sendfulfil(form){

    // Get arguments.
    var proposalhash = form.find('select.proposalhash').val();
    var proposal = proposals[proposalhash];
    var give = form.find('div.give');
    give = {
        'colordef': give.find('select.colordef').val(),
        'quantity': give.find('input.quantity').val(),
        'utxos': $.parseJSON(give.find('textarea.utxos').val()),
        'pvtkeys': $.parseJSON(give.find('input.pvtkeys').val()),
        'address': proposal['take']['address']
    };
    var take = form.find('div.take');
    take = {
        'colordef': take.find('select.colordef').val(),
        'quantity': take.find('input.quantity').val(),
        'address': take.find('input.address').val()
    };

    // Create transaction specification.
    var txspec = {};
    txspec.inputs = {};
    txspec.inputs[proposal.give.colordef] = $.map(
        proposal.give.utxos, txobj2tuple
    );
    txspec.inputs[give.colordef] = $.map(
        give.utxos, txobj2tuple
    );

    txspec.targets = [
        [
            give.address,
            give.colordef,
            give.quantity
        ], [
            take.address,
            take.colordef,
            take.quantity
        ]
    ];

    jsonp('makeconversion', {'txspec': JSON.stringify(txspec)}, function(tx){
        jsonp(
            'signrawtransaction',
            {
                'rawtx': tx.hex,
                'inputs': $.merge(proposal.give.utxos, give.utxos),
                'keys': give.pvtkeys
            },
            function(tx){
                log(
                    (tx.complete ? 'completely' : 'partially') + ' signed',
                    tx.hex
                );
                var fulfil = {
                    'proposalhash': proposalhash,
                    'utxos': give.utxos,
                    'hex': tx.hex
                };
                jsonp(
                    'send',
                    {
                        'subject': 'fulfil',
                        'body': JSON.stringify(fulfil)
                    },
                    function(msgid){
                        log('sending fulfil in msg ' + msgid, fulfil);
                    }
                );
            }
        );
    });
}

// Accepts a fulfil.
function acceptfulfil(form){

    // Get arguments.
    var fulfilhash = form.find('select.fulfilhash').val();
    var fulfil = fulfils[fulfilhash];
    var hex = fulfil.hex;
    var proposalhash = fulfil.proposalhash;
    var proposal = proposals[proposalhash];
    var give = form.find('div.give');
    give = {
        'colordef': give.find('select.colordef').val(),
        'quantity': give.find('input.quantity').val(),
        'utxos': $.parseJSON(give.find('textarea.utxos').val()),
        'pvtkeys': $.parseJSON(give.find('input.pvtkeys').val())
    };
    var take = form.find('div.take');
    take = {
        'colordef': take.find('select.colordef').val(),
        'quantity': take.find('input.quantity').val(),
        'address': take.find('input.address').val()
    };

    jsonp(
        'signrawtransaction',
        {
            'rawtx': tx.hex,
            'inputs': fulfil.utxos,
            'keys': give.pvtkeys
        },
        function(tx){
            log(
                (tx.complete ? 'completely' : 'partially') + ' signed',
                tx.hex
            );
            jsonp('sendrawtransaction', {'rawtx': tx.hex}, function(txid){
                jsonp(
                    'send',
                    {
                        'subject': 'accept',
                        'body': JSON.stringify({
                            'fulfilhash': fulfilhash,
                            'txid': txid,
                            'hex': tx.hex
                        })
                    },
                    function(msgid){
                        log('sending accept in msg ' + msgid, fulfilhash, tx.hex);
                    }
                );
            });
        }
    );
}

var marketdiv;
var pairskelaton;
$(function(){
    $('#nojs').remove();

    // Get some useful elements.
    marketdiv = $('#market');
    pairskelaton = $('.pair').remove().show();

    // Replace others.
    colorchoice($('input.colordef'));
    proposalchoice();
    fulfilchoice();

    // Bind proposal and fulfil send buttons.
    $('#sendproposal').click(function(e){sendproposal($(this).parent());});
    $('#sendfulfil').click(function(e){sendfulfil($(this).parent());});
    $('#acceptfulfil').click(function(e){acceptfulfil($(this).parent());});

    // Start getting messages.
    getmessages();
});
