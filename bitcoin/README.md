Bitcoin module
==============

The module needs to implement a single function:

- signrawtransaction(rawtx, txinputs, privatekeys)

The function tries to sign the transaction, and to broadcast it to the bitcoin
network if it is fully signed. It returns an object with the full hex of the
signed transaction, an indicator of completeness, and - if the transaction was
broadcasted - its txid.

We are experimenting with using bitcoinj, for SPV support, and we hope to soon
add some tips and tricks here, but at the moment we are running with bitcoind.

The module runs bitcoind automatically on startup, with the configuration file
setting the RPC user and password and making sure you are running on testnet
(we do not want to accidentally run this with a mainnet wallet - it is not
safe) and also implements the close function that shuts it down.

To make this work on Windows, or other platforms you will need to change the
`Popen` call according to whatever you have installed.

Note that the configuration file has bitcoind running with full transaction
index (`txindex = 1` This is not required, it just seems to be the most common
setting amongst CC devs. If bitcoind complains about reindexing, removing this
line will probably solve your problem.

Protip: using [freewil](https://github.com/freewil)'s easy mining fork on an
internal net can come very handy when testing.
