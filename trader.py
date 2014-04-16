#!/usr/bin/python3

import jsonrpclib
colorserver = jsonrpclib.Server('http://127.0.0.1:6711')
print('Connected to color server with no introspection')

red = 'obc:8a78b017ea9d97ca7d1044fc9b3bc40356518a9fe68a4466197c0f22d2e29e82:0:209609'
blue = 'obc:6beaf35c6b4fbb8dfa0c4a1483e90ecd06d2ecbd4a05b2dbe92a480acd4ad2fe:0:209610'
aliceunspentred = [['8a78b017ea9d97ca7d1044fc9b3bc40356518a9fe68a4466197c0f22d2e29e82', 0], ['8a78b017ea9d97ca7d1044fc9b3bc40356518a9fe68a4466197c0f22d2e29e82', 1]]
bobunspentblue = [['6beaf35c6b4fbb8dfa0c4a1483e90ecd06d2ecbd4a05b2dbe92a480acd4ad2fe', 0]]
aliceblueaddress = '6ZNFj4EMrvWHCD@mrSU1wpXhpZHcj7kfyzuSkzBHqhgRCD3vx'
bobredaddress = '9Xs9thPERNq2Yw@mvppS4uMXqpq46W5jFPXpPcXLrtNmEG2zJ'

print(
    {
        'inputs': {
            red: aliceunspentred,
            blue: bobunspentblue
        },
        'targets': [
            [
                aliceblueaddress,
                blue,
                1
            ], [
                bobredaddress,
                red,
                10
            ]
        ]
    },
    {
        'color_spec': red,
        'value': 10
    },
    {
        'color_spec': blue,
        'value': 1
    }
)


tx = colorserver.makeconversion(
    {
        'inputs': {
            red: aliceunspentred,
            blue: bobunspentblue
        },
        'targets': [
            [
                aliceblueaddress,
                blue,
                1
            ], [
                bobredaddress,
                red,
                10
            ]
        ]
    },
    {
        'color_spec': red,
        'value': 10
    },
    {
        'color_spec': blue,
        'value': 1
    }
)

lamapo

print('Bob got proposal and sent a fulfil: ', msgserver.send('fulfil', tx))






msgserver = jsonrpclib.Server('http://127.0.0.1:6712')
print("Connected to message server with functions: %s" % (', '.join(msgserver.system.listMethods())))

# Here ars definitions of red and blue from chromawallet:
#{"color_set": ["obc:6beaf35c6b4fbb8dfa0c4a1483e90ecd06d2ecbd4a05b2dbe92a480acd4ad2fe:0:209610"], "monikers": ["blue"], "unit": 1}
#{"color_set": ["obc:8a78b017ea9d97ca7d1044fc9b3bc40356518a9fe68a4466197c0f22d2e29e82:0:209609"], "monikers": ["red"], "unit": 1}
red = 'obc:8a78b017ea9d97ca7d1044fc9b3bc40356518a9fe68a4466197c0f22d2e29e82:0:209609'
blue = 'obc:6beaf35c6b4fbb8dfa0c4a1483e90ecd06d2ecbd4a05b2dbe92a480acd4ad2fe:0:209610'

# Alice owns some red coins, here is her red UTXO list (and I'm adding a fake one, to test the color server):
aliceunspentred = [['8a78b017ea9d97ca7d1044fc9b3bc40356518a9fe68a4466197c0f22d2e29e82', 0], ['8a78b017ea9d97ca7d1044fc9b3bc40356518a9fe68a4466197c0f22d2e29e82', 1]]
# And she wishes to sell 10 of them for 1 blue coins, so here is her blue address:
aliceblueaddress = '6ZNFj4EMrvWHCD@mrSU1wpXhpZHcj7kfyzuSkzBHqhgRCD3vx'
# That's enough to create a proposal.
print('Alice sent proposal: ', msgserver.send('proposal', {
    'give': {
        'asset': red,
        'quantity': 10,
        'utxos': aliceunspentred
    },
    'take': {
        'asset': blue,
        'quantity': 1,
        'address': aliceblueaddress
    }
}))

# And then comes bob, who has blue coins, here is his blue UTXO list:
bobunspentblue = [['6beaf35c6b4fbb8dfa0c4a1483e90ecd06d2ecbd4a05b2dbe92a480acd4ad2fe', 0]]
# And he wants 10 red coins, here is his red address:
bobredaddress = '9Xs9thPERNq2Yw@mvppS4uMXqpq46W5jFPXpPcXLrtNmEG2zJ'
# So he listens for a proposal he likes.
print('Bob is waiting for the proposal')
def waitforproposal():
    while True:
        for msg in msgserver.receive():
            try:
                if 'proposal' == msg['subject']:
                    proposal = msg['body']
                    give = proposal['give']
                    take = proposal['take']

                    give['verifiedquantity'] = 0
                    for utxo in give['utxos']:
                        try: give['verifiedquantity'] += colorserver.colorvalue(red, utxo)
                        except jsonrpclib.jsonrpc.ProtocolError: continue

                    if (
                        blue == take['asset'] and
                        1 == take['quantity'] and
                        red == give['asset'] and
                        10 == give['quantity'] and
                        10 <= give['verifiedquantity']
                    ):
                        tx = colorserver.makeconversion({
                            'inputs': {
                                red: give['utxos'],
                                blue: bobunspentblue
                            },
                            'targets': [
                                [
                                    take['address'],
                                    take['asset'],
                                    take['quantity']
                                ], [
                                    bobredaddress,
                                    red,
                                    10
                                ]
                            ]
                        })
                        print('Bob got proposal and sent a fulfil: ', msgserver.send('fulfil', tx))
                        return
            except KeyError: pass
waitforproposal()

# Alice waits till she hears an offer she likes
print('Alice is waiting for the fulfil')
def waitforfulfil():
    while True:
        for msg in msgserver.receive():

            # Alice should really use the color server to check if she likes the transaction, but for now she will just jump at the first fulfil. And does nothing with it. And lies about it.
            try:
                if 'fulfil' == msg['subject']:
                    print('Alice is signing the transction and broadcasting it')
                    return
            except KeyError: pass
waitforfulfil()

# Soon we will need these too!
#bobblueaddress = '6ZNFj4EMrvWHCD@mojeSSh6zghf2kSeCUGTj1FbuMniXeXmS8'
#aliceredaddress = '9Xs9thPERNq2Yw@mtvwhPxwXwwzMdSi6keubo5UXHuR6LJtmG'
