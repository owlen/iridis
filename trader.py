#!/usr/bin/python3

import jsonrpclib
msgserver = jsonrpclib.Server('http://127.0.0.1:6712')
print("Connected to message server with functions: %s" % (', '.join(msgserver.system.listMethods())))
colorserver = jsonrpclib.Server('http://127.0.0.1:6711')
print("Connected to color server with functions: %s" % (', '.join(colorserver.system.listMethods())))

# Here ars issuances of red and blue from chromawallet:
unspentred = ['8a78b017ea9d97ca7d1044fc9b3bc40356518a9fe68a4466197c0f22d2e29e82', 1]
unspentblue = ['6beaf35c6b4fbb8dfa0c4a1483e90ecd06d2ecbd4a05b2dbe92a480acd4ad2fe', 1]

# And here is a JSON that defines it, according to the mastercoin definitions: https://github.com/mastercoin-MSC/spec/blob/master/AssetIssuanceStandard.md
# TODO: Create to JSONs for red and blue, and start using them.
colordef = {
    "name": "Credit at John Doe's",
    "name_short": "JD Credits",
    "issuer": "John Doe's Restaurant Chain",
    "type": "Credit",
    "currency": "USD",
    "description": "Can be used for any purchase at John Doe's, excluding breakfasts.",

    "interest_rate": 1,
    "issue_date": "2014-03-01",
    "expiry_date": "2024-02-29",

    "icon_url": "http://www.john-doe-dining.com/bitcoin-credits-icon.png",
    "image_url": "http://www.john-doe-dining.com/bitcoin-credits-image.png",
    "contract_url": "http://www.john-doe-dining.com/bitcoin-credits-contract.pdf",
    "redemption_url": "http://www.john-doe-dining.com/bitcoin-credits-redeem.php",
    "feed_url": "http://www.john-doe-dining.com/bitcoin-credits-feed.rss",

    "color": "#ffccaa",
    "multiple": 0.01,
    "format": "* dollars",
    "format_1": "1 dollar",

    "mastercoin_id": "123456",
    "coinprism_sources": ["2MyvmsxoCxsnzPapDnK7ZcMxWjU3hqLZkpX"],
    "coincolors_id": "f5d8ee39a430901c91a5917b9f2dc19d6d1a0e9cea205b009ca73dd04470b9a6"
}

# Alice owns the red coins, and wishes to sell 10 of them for 10 blue coins.
# Note that offeredOutputs is a list of unspent outputs, while requestedAsset is a single blue output, and can be any such output, even a spent one. It is just a way to represent a color.
print('Alice sent proposal: ', msgserver.send('proposal', {
    'offeredOutputs': [unspentred],
    'quantityOffered': 10,
    'requestedAsset': unspentblue,
    'price': 1
}))

# Bob waits till he hears a proposal he likes
print('Bob is waiting for the proposal')
def waitforproposal():
    while True:
        for msg in msgserver.receive():

            # Bob should really use the colorserver to check if the all the offeredOutputs are of a color and quantity he likes, but for now we just check for the one transaction we know about.
            try:
                if unspentred == msg['body']['offeredOutputs'][0]:
                    print('Bob got proposal and sent a fulfil: ', msgserver.send('fulfil', {'hex': '0100000001aca7f3b45654c230e0886a57fb988c3044ef5e8f7f39726d305c61d5e818903c00000000fd5d010048304502200187af928e9d155c4b1ac9c1c9118153239aba76774f775d7c1f9c3e106ff33c0221008822b0f658edec22274d0b6ae9de10ebf2da06b1bbdaaba4e50eb078f39e3d78014730440220795f0f4f5941a77ae032ecb9e33753788d7eb5cb0c78d805575d6b00a1d9bfed02203e1f4ad9332d1416ae01e27038e945bc9db59c732728a383a6f1ed2fb99da7a4014cc952410491bba2510912a5bd37da1fb5b1673010e43d2c6d812c514e91bfa9f2eb129e1c183329db55bd868e209aac2fbc02cb33d98fe74bf23f0c235d6126b1d8334f864104865c40293a680cb9c020e7b1e106d8c1916d3cef99aa431a56d253e69256dac09ef122b1a986818a7cb624532f062c1d1f8722084861c5c3291ccffef4ec687441048d2455d2403e08708fc1f556002f1b6cd83f992d085097f9974ab08a28838f07896fbab08f39495e15fa6fad6edbfb1e754e35fa1c7844c41f322a1863d4621353aeffffffff0140420f00000000001976a914ae56b4db13554d321c402db3961187aed1bbed5b88ac00000000'}))
                    return
            except KeyError: pass
waitforproposal()

# Alice waits till she hears an offer she likes
print('Alice is waiting for the fulfil')
def waitforfulfil():
    while True:
        for msg in msgserver.receive():

            # Alice should really use the colorserver to check if she likes the transaction, but for now she will just jump at the first fulfil.
            try:
                if 'fulfil' == msg['subject']:
                    print('Alice is signing the transction and broadcasting it')
                    return
            except KeyError: pass
waitforfulfil()
