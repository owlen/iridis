#!/usr/bin/python3

# Connect to a patched ngccc-server on port 6711:
# https://github.com/israellevin/ngcccbase
# and expose colorvalue and maketransaction

from jsonrpclib import Server
colorserver = Server('http://127.0.0.1:6711')

def colorvalue(colordef, utxo): return colorserver.colorvalue(colordef, utxo)

def makeconversion(txspec): return colorserver.makeconversion(txspec)

def close(): pass
