#!/usr/bin/python3

# This module takes all the services required for colored trading and unites
# them under one API, as a JSON-RPC server that can be accessed from a browser.

# Since we are going to run some processes, let's make sure we exit cleanly
from atexit import register
def close():
    print("\nshutting down")
    message.close()
register(close)

# Then we can import the actual functionality
import  message

# And run a server that exposes it
if __name__ == '__main__':

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
    address = ('localhost', 6710)
    server = SimpleJSONRPCServer(address, Handler)

    # Register functions
    server.register_introspection_functions()
    server.register_function(message.send, 'send')
    server.register_function(message.receive, 'receive')

    # Serve RPC
    print("Serving JSON on http://%s:%i ..." % address)
    try:
        server.serve_forever()

    # Shut down
    except KeyboardInterrupt:
        from sys import exit
        exit(0)
