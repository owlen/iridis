#!/usr/bin/python3

# Create interfaces to color, message and bitcoind servers
import jsonrpclib
colorserver = jsonrpclib.Server('http://127.0.0.1:6711')
print('Connected to color server with no introspection')
msgserver = jsonrpclib.Server('http://127.0.0.1:6712')
print("Connected to message server with functions: %s" % (', '.join(msgserver.system.listMethods())))
btcserver = jsonrpclib.Server('http://user:pass@127.0.0.1:18332')
print("Connected to bitcoind server with no introspection: %s" % (btcserver))

# Here ars definitions of red and blue from chromawallet:
#{"color_set": ["obc:6beaf35c6b4fbb8dfa0c4a1483e90ecd06d2ecbd4a05b2dbe92a480acd4ad2fe:0:209610"], "monikers": ["blue"], "unit": 1}
#{"color_set": ["obc:8a78b017ea9d97ca7d1044fc9b3bc40356518a9fe68a4466197c0f22d2e29e82:0:209609"], "monikers": ["red"], "unit": 1}
red = 'obc:8a78b017ea9d97ca7d1044fc9b3bc40356518a9fe68a4466197c0f22d2e29e82:0:209609'
blue = 'obc:6beaf35c6b4fbb8dfa0c4a1483e90ecd06d2ecbd4a05b2dbe92a480acd4ad2fe:0:209610'

# Alice owns some red coins, here is her red UTXO list (and I'm adding a fake one, to test the color server):
aliceunspentred = [['8a78b017ea9d97ca7d1044fc9b3bc40356518a9fe68a4466197c0f22d2e29e82', 0], ['8a78b017ea9d97ca7d1044fc9b3bc40356518a9fe68a4466197c0f22d2e29e82', 1]]
# And she wishes to sell 10 of them for 1 blue coins, so here is her blue address:
aliceblueaddress = 'mrSU1wpXhpZHcj7kfyzuSkzBHqhgRCD3vx'
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
    },
    'scheme': 1
}))

# And then comes bob, who has blue coins, here is his blue UTXO list:
bobunspentblue = [['6beaf35c6b4fbb8dfa0c4a1483e90ecd06d2ecbd4a05b2dbe92a480acd4ad2fe', 0]]
# And he wants 10 red coins, here is his red address:
bobredaddress = 'mvppS4uMXqpq46W5jFPXpPcXLrtNmEG2zJ'

print('Bob is waiting for the proposal')
def waitforproposal():
    while True:
        for msg in msgserver.receive():
            try:
                if 'proposal' == msg['subject']:
                    proposal = msg['body']
                    give = proposal['give']
                    take = proposal['take']

                    # Sum up the values of the UTXOs
                    give['verifiedquantity'] = 0
                    for utxo in give['utxos']:
                        try:
                            val = colorserver.colorvalue(red, utxo)
                            if isinstance(val, int): give['verifiedquantity'] += val
                        except jsonrpclib.jsonrpc.ProtocolError: continue

                    if (
                        blue == take['asset'] and
                        1 == take['quantity'] and
                        red == give['asset'] and
                        10 == give['quantity'] and
                        10 <= give['verifiedquantity']
                    ):

                        # Bob creates a color conversion tx (with signed fee)
                        tx = colorserver.makeconversion(
                            {
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

                        # Bob signs his inputs
                        bobprvkeys = ['93NgLRXNYohxTM5z7Ug3wiAqHDLRC7LDLPWmzqkqpzfVRu7Gcbj', '92MBwPBZMrGcaDTRp2pGJHC5oXEMucHymWhGqcZ6Da2pNwoGbfL']
                        inputs = []
                        for utxo in bobunspentblue:
                            parenttx = btcserver.getrawtransaction(utxo[0])
                            parenttx = btcserver.decoderawtransaction(parenttx)
                            scrpubk = parenttx['vout'][utxo[1]]['scriptPubKey']['hex']
                            inputs.append({'txid': utxo[0], 'vout': utxo[1], 'scriptPubKey': scrpubk})
                        tx = btcserver.signrawtransaction(tx['hex'], inputs, bobprvkeys)

                        print('Bob got proposal and sent a fulfil: ', msgserver.send('fulfil', {
                            'take': {
                                'asset': red,
                                'quantity': 10,
                                'utxos': aliceunspentred,
                                'address': bobredaddress
                            },
                            'give': {
                                'asset': blue,
                                'quantity': 1,
                                'utxos': bobunspentblue,
                                'address': aliceblueaddress
                            },
                            'tx': tx['hex']
                            }))
                        return
            except KeyError: pass
waitforproposal()

print('Alice is waiting for the fulfil')
def waitforfulfil():
    while True:
        for msg in msgserver.receive():
            print(msg)
            try:
                if 'fulfil' == msg['subject']:
                    fulfil = msg['body']
                    give = fulfil['give']
                    take = fulfil['take']
                    rawtx = fulfil['tx']
                    tx = btcserver.decoderawtransaction(rawtx)

                    # Sum up the values of the UTXOs
                    give['verifiedquantity'] = 0
                    take['verifiedquantity'] = 0
                    inputs = []
                    for utxo in tx['vin']:
                        print(1, utxo)
                        try:
                            val = colorserver.colorvalue(blue, (utxo['txid'], utxo['vout']))
                            if isinstance(val, int): give['verifiedquantity'] += val
                            else:
                                val = colorserver.colorvalue(red, (utxo['txid'], utxo['vout']))
                                if isinstance(val, int):
                                    take['verifiedquantity'] += val

                                    # If I'm here, I might as well collect the inputs I'm gonna sign
                                    parenttx = btcserver.getrawtransaction(utxo['txid'])
                                    parenttx = btcserver.decoderawtransaction(parenttx)
                                    scrpubk = parenttx['vout'][utxo[1]]['scriptPubKey']['hex']
                                    inputs.append({'txid': utxo[0], 'vout': utxo[1], 'scriptPubKey': scrpubk})
                        except jsonrpclib.jsonrpc.ProtocolError: continue

                    # Make sure she likes the offer
                    if (
                        red == take['asset'] and
                        10 == take['quantity'] and
                        10 >= take['verifiedquantity'] and
                        blue == give['asset'] and
                        1 == give['quantity'] and
                        1 <= give['verifiedquantity']
                    ):

                        # Alice signs her inputs
                        aliceprvkeys = ['93Hr5v7yk7e8KJvyhPnLhAEiotaczmVjn4SC212bTJL6im7xK4s', '92jwJEE8giVMxhUx9T2kCo5rW6RBvQfEKcySWtRV8tmxjc2ig2f', '92Mqi7Fp2n5JAxAHwhQ3HEU3bkfVxD5cjtd7W8K9wtumwat1rRd']
                        tx = btcserver.signrawtransaction(rawtx, inputs, aliceprvkeys)

                        print(
                            'Alice is signing the transction and broadcasting it',
                            btcserver.sendrawtransaction(tx['hex'])
                        )
                        return
            except KeyError: pass
waitforfulfil()

# Soon we will need these too!
#(bobblueaddress = 'mojeSSh6zghf2kSeCUGTj1FbuMniXeXmS8'
#aliceredaddress = 'mtvwhPxwXwwzMdSi6keubo5UXHuR6LJtmG'
# Make give and take consistent, maybe with atob and btoa, or proposal to fulfil or something.
