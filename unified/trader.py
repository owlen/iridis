#!/usr/bin/python3

# This module takes all the services required for colored trading and unites
# them under one API, as a JSON-RPC server that can be accessed from a browser.
if __name__ == '__main__':

    # Get the actual functionality
    import colorfunctions, messagefunctions, bitcoinfunctions

    # Create a request handler that will serve OPTION requests and allow any origin
    from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCRequestHandler
    class Handler(SimpleJSONRPCRequestHandler):
        def do_OPTIONS(self):
            self.send_response(200, "ok")
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-Type")
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'X-Requested-With')
            self.end_headers()

    # Create server
    from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
    address = ('127.0.0.1', 6710)
    server = SimpleJSONRPCServer(address, Handler)

    # Register functions
    server.register_introspection_functions()
    server.register_function(colorfunctions.colorvalue, 'colorvalue')
    server.register_function(colorfunctions.makeconversion, 'makeconversion')
    server.register_function(messagefunctions.send, 'send')
    server.register_function(messagefunctions.receive, 'receive')
    server.register_function(bitcoinfunctions.getscriptpubkey, 'getscriptpubkey')
    server.register_function(bitcoinfunctions.signrawtransaction, 'signrawtransaction')

    # Serve RPC
    print("Serving JSON on %s:%i" % address)
    try:
        server.serve_forever()

    # Shut down
    except KeyboardInterrupt:
        print("\nshutting down")
        colorfunctions.close()
        messagefunctions.close()
        bitcoinfunctions.close()
        from sys import exit
        exit(0)
