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

    # Create a cross domain request handler (with OPTIONS request) that serves
    # JSON on post and JSONp + files on GET
    from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCRequestHandler
    from http.server import SimpleHTTPRequestHandler
    from urllib.parse import urlparse, parse_qs
    from json import dumps
    class Handler(SimpleHTTPRequestHandler, SimpleJSONRPCRequestHandler):
        def do_OPTIONS(self):
            self.send_response(200, 'ok')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
            self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'X-Requested-With')
            self.end_headers()

        def do_GET(self):
            # Parse query string, make sure we have a callback.
            url = urlparse(self.path)
            if '.jsonp' != url.path[-6:]: return SimpleHTTPRequestHandler.do_GET(self)
            query = parse_qs(url.query)
            if 'callback' not in query: raise Exception('No callback specified')
            callback = query['callback'][-1]

            # Get data for different JSONp calls
            try:
                if '/colorvalue.jsonp' == url.path:
                    colordef = query['colordef'][0]
                    txo = query['txo']
                    data = color.colorvalue(colordef, txo)
                else:
                    data = {'error': 'Did not understand ' + url.path}

            except (KeyError, ValueError): data = {'error': 'Wrong parameters', 'query': query}

            # Send the reply as jsonp
            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.end_headers()
            self.wfile.write(bytes(callback + '(' + dumps(data) + ');', 'UTF-8'))

    # Create server
    from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
    server = SimpleJSONRPCServer(('', 6710), Handler)

    # Register functions
    server.register_introspection_functions()
    server.register_function(color.colorvalue, 'colorvalue')
    server.register_function(color.makeconversion, 'makeconversion')
    server.register_function(message.send, 'send')
    server.register_function(message.receive, 'receive')
    server.register_function(bitcoin.signrawtransaction, 'signrawtransaction')

    # Serve RPC
    sockname = server.socket.getsockname()
    print("\nServing JSON, JSONp and HTTP on", sockname[0], "port", sockname[1], "...")
    try:
        server.serve_forever()

    # Shut down
    except KeyboardInterrupt:
        from sys import exit
        exit(0)
