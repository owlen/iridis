Color server
============

The server needs to implement the following two JSON-RPC calls:

- colorvalue(colordef, utxo) - returns the unspent color value of utxo (a tuple in the form (txhash, outputindex)) if it is of color colordef, or false if it is not.
- makeconversion(txspec, our, their) - returns a raw color conversion transaction according to txspec. The other two parameters are a patchy leftover and will soon be removed.
