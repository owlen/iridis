#!/usr/bin/python3

# Connect to a patched ngccc-server on port 6711:
# https://github.com/israellevin/ngcccbase
# and expose colorvalue and maketransaction


# Make sure the port is available
port = 6711
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if 0 == sock.connect_ex(('localhost', port)):
    sock.close()
    raise Exception("port %d is in use, aborting" % (port,))

# Run ngccc-server
from subprocess import Popen, PIPE
from os import path
curpath = path.dirname(path.abspath(__file__))
ngcccprocess = Popen(('python', curpath + '/ngcccbase/ngccc-server.py', 'localhost', str(port)), stdout=PIPE)

# Connect to its JSON-RPC server
from jsonrpclib import Server
colorserver = Server("http://127.0.0.1:%d" % (port,))

# Implement required functionality
def colorvalue(colordef, txo): return colorserver.colorvalue(colordef, txo)
def makeconversion(txspec): return colorserver.makeconversion(txspec)
def close(): ngcccprocess.terminate()
