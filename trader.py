#!/usr/bin/python3

# This module takes all the services required for colored trading and unites
# them under one API, as a JSON-RPC server that can be accessed from a browser.

# Since we are going to run some processes, let's make sure we exit cleanly
from atexit import register
def close():
    print("\nshutting down")
    color.close()
    message.close()
    bitcoin.close()
register(close)

# Then we can import the actual functionality
import color, message, bitcoin

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
    server.register_function(color.colorvalue, 'colorvalue')
    server.register_function(color.makeconversion, 'makeconversion')
    server.register_function(message.send, 'send')
    server.register_function(message.receive, 'receive')
    server.register_function(bitcoin.signrawtransaction, 'signrawtransaction')

    # Spawn web server, and make sure you close it at exit
    from subprocess import Popen, DEVNULL
    from os import path
    curpath = path.dirname(path.abspath(__file__))
    webserverprocess = Popen(('python3', '-m', 'http.server'), stdout=DEVNULL)
    register(lambda: webserverprocess.terminate())

    # Serve RPC
    print("Serving JSON on http://%s:%i and HTTP on http://%s:%i ..." % (address + (address[0], 8000)))
    try:
        server.serve_forever()

    # Shut down
    except KeyboardInterrupt:
        from sys import exit
        exit(0)
