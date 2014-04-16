#!/usr/bin/python3

import jsonrpclib
colorserver = jsonrpclib.Server('http://127.0.0.1:6711')
print("Connected to color server with functions: %s" % (', '.join(colorserver.system.listMethods())))
msgserver = jsonrpclib.Server('http://127.0.0.1:6712')
print("Connected to message server with functions: %s" % (', '.join(msgserver.system.listMethods())))

# Here ars definitions of red and blue from chromawallet:
#{"color_set": ["obc:6beaf35c6b4fbb8dfa0c4a1483e90ecd06d2ecbd4a05b2dbe92a480acd4ad2fe:0:209610"], "monikers": ["blue"], "unit": 1}
#{"color_set": ["obc:8a78b017ea9d97ca7d1044fc9b3bc40356518a9fe68a4466197c0f22d2e29e82:0:209609"], "monikers": ["red"], "unit": 1}
red = 'obc:8a78b017ea9d97ca7d1044fc9b3bc40356518a9fe68a4466197c0f22d2e29e82:0:209609'
blue = 'obc:6beaf35c6b4fbb8dfa0c4a1483e90ecd06d2ecbd4a05b2dbe92a480acd4ad2fe:0:209610'

# Alice owns some red coins, here is her red UTXO list:
aliceunspentred = [['8a78b017ea9d97ca7d1044fc9b3bc40356518a9fe68a4466197c0f22d2e29e82', 0]]
# And she wishes to sell 10 of them for 1 blue coins, so here is her blue address:
aliceblueaddress = '6ZNFj4EMrvWHCD@mrSU1wpXhpZHcj7kfyzuSkzBHqhgRCD3vx'
# That's enough to create a proposal.
#print('Alice sent proposal: ', msgserver.send('proposal', {
#    'give': {
#        'asset': red,
#        'quantity': 10,
#        'utxos': aliceunspentred
#    },
#    'take': {
#        'asset': blue,
#        'quantity': 1,
#        'address': aliceblueaddress
#    }
#}))

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
                    if (
                        blue == take['asset'] and
                        1 == take['quantity'] and
                        red == give['asset'] and
                        10 == give['quantity'] and
                        10 <= sum(
                            colorserver.getoutputvalue(utxo, red)['colorvalue'] for utxo in give['utxos']
                        )
                    ):
                        # TODO Construct an actual partially signed transaction with colorlib
                        tx = {
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
                        }
                        print(colorserver.makeconversion(tx))
                        stophere

                        print('Bob got proposal and sent a fulfil: ', msgserver.send('fulfil', {'hex': '0100000001aca7f3b45654c230e0886a57fb988c3044ef5e8f7f39726d305c61d5e818903c00000000fd5d010048304502200187af928e9d155c4b1ac9c1c9118153239aba76774f775d7c1f9c3e106ff33c0221008822b0f658edec22274d0b6ae9de10ebf2da06b1bbdaaba4e50eb078f39e3d78014730440220795f0f4f5941a77ae032ecb9e33753788d7eb5cb0c78d805575d6b00a1d9bfed02203e1f4ad9332d1416ae01e27038e945bc9db59c732728a383a6f1ed2fb99da7a4014cc952410491bba2510912a5bd37da1fb5b1673010e43d2c6d812c514e91bfa9f2eb129e1c183329db55bd868e209aac2fbc02cb33d98fe74bf23f0c235d6126b1d8334f864104865c40293a680cb9c020e7b1e106d8c1916d3cef99aa431a56d253e69256dac09ef122b1a986818a7cb624532f062c1d1f8722084861c5c3291ccffef4ec687441048d2455d2403e08708fc1f556002f1b6cd83f992d085097f9974ab08a28838f07896fbab08f39495e15fa6fad6edbfb1e754e35fa1c7844c41f322a1863d4621353aeffffffff0140420f00000000001976a914ae56b4db13554d321c402db3961187aed1bbed5b88ac00000000'}))
                        return
            except KeyError: pass
waitforproposal()

# Alice waits till she hears an offer she likes
print('Alice is waiting for the fulfil')
def waitforfulfil():
    while True:
        for msg in msgserver.receive():

            # Alice should really use the colorserver to check if she likes the transaction, but for now she will just jump at the first fulfil. And does nothing with it. And lies about it.
            try:
                if 'fulfil' == msg['subject']:
                    print('Alice is signing the transction and broadcasting it')
                    return
            except KeyError: pass
waitforfulfil()

#bobblueaddress = '6ZNFj4EMrvWHCD@mojeSSh6zghf2kSeCUGTj1FbuMniXeXmS8'
#aliceredaddress = '9Xs9thPERNq2Yw@mtvwhPxwXwwzMdSi6keubo5UXHuR6LJtmG'
#ROTEM - arraymap jsonobject
