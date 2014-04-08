#!/usr/bin/python3

def getvoutcolor(vout):
    return {
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

def makeconversion(sieve):
    return { 'hex': 'tx' }

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
server = SimpleJSONRPCServer(('127.0.0.1', 6711))
server.register_introspection_functions()
server.register_function(getvoutcolor, 'getvoutcolor')
server.register_function(makeconversion, 'makeconversion')
print('Serving JSON on 6711')
try:
    server.serve_forever()
except KeyboardInterrupt:
    from sys import exit
    exit(0)
