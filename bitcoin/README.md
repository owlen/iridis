Bitcoin server
==============

The server needs to implement the following four JSON-RPC calls:

- getrawtransaction(txid)
- decoderawtransaction(rawtx)
- signrawtransaction(rawtx, txinputs, privatekeys)
- sendrawtransaction(rawtx)

We are experimenting with using bitcoinj, for SPV support, and we hope to soon add some tips and tricks here, but at the moment our tests require bitcoind running with full txindex (txindex = 1).

Protip: using [freewil](https://github.com/freewil)'s easy mining fork on an internal bitcoin net can come very handy when testing.
