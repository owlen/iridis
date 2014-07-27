#!/usr/bin/python3

# Shake your market maker - iridis style.

# In the future this will come from a different module.
# Indented for folding.
if True:
	colors = {
		'usd': {
			'price': 1,
			'colordef': 'usd'
		},
		'eur': {
			'price': 1.35,
			'colordef': 'eur'
		},
		'gold': {
			'price': 1300,
			'colordef': 'gld'
		},
		'silver': {
			'price': 20,
			'colordef': 'slv'
		},
		'btc': {
			'price': 600,
			'colordef': ''
		}
	}
	def pairprice(color1, color2):
		return float(color1['price']) / float(color2['price'])

# Since we are going to run some processes, let's make sure we exit cleanly
from atexit import register as addtoexit
def close():
    print("\nshutting down")
    # color.close()
    message.close()
    bitcoin.close()
addtoexit(close)

# Then we can import the actual functionality
import message, bitcoin #, color

# build our API:
proposal = {
	'scheme': -1,
	'version': -1,
	'KYC':[
		#'1B1bE3ctpkkJHvCT5SwXUyzxUojFfQhZCz'
	],
	'give':{
		'colordef': '',
		'quantity': 0,
		'utxos':[
			{
				'txid': '',
				'vout': 0,
				'scriptPubKey': ''
			}
		]
	},
	'take':{
		'colordef': '',
		'quantity': 0,
		'address': ''
	}
}	

def setcolor(colorname, price, colordef=None):
	if colorname in colors:
		colors[colorname].price = price
		if not colordef is None:
			colors[colorname].colordef = colordef
	elif not colordef is None:
		colors[colorname] = { 'price': price, 'colordef': colordef }
	else:
		raise ValueError('Color not found and can\'t be created')
		
proposals = []
def getmyproposals():
	return proposals

def propose(proposal):
	return message.send('proposal', proposal)
	
def cancelproposal(proposalhash):
	proposals.append(proposal)
	#TODO add proposal hash
	return message.send('cancel', proposalhash)

# And run a server that exposes it
if __name__ == '__main__':
	
    # Create server
    from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
    server = SimpleJSONRPCServer(('', 6710))

    # Register functions
    server.register_introspection_functions()
    server.register_function(setcolor, 'setcolorvalue')
    server.register_function(getmyproposals, 'getmyproposals')
    server.register_function(propose, 'propose')
    server.register_function(cancelproposal, 'cancelproposal')

    # Serve RPC till exit
    addtoexit(server.shutdown)
    sockname = server.socket.getsockname()
    print("\nServing JSON, JSONp and HTTP on", sockname[0], "port", sockname[1], "...")
    try:
        server.serve_forever()

    # Shut down
    except KeyboardInterrupt:
        from sys import exit
        exit(0)