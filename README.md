ematadoro
=========

Framework for decentralized conversion of colored coins.

## color.py ##

- getvoutcolor(vout) -> color, amount
- makeconversion(color, amount1, key, vouts, amount2) -> a tx that transfers amount of color (signed with key) to the address of vouts, and amount2 from vouts to key's address (unsigned)

## messages.py ##

- listen(filter) -> list of matching propositions, list of matching offers
- propose(filter) -> success of broadcasting proposition to the network
- offer(tx) -> success of broadcasting offer to the network

## trader.py ##

1. Receive user preferences (UI)
1. Construct matching filters
1. Listen for any matching propositions (messaging network)
1. Validate their vouts (colorlib)
1. Construct matching offers (colorlib) and send them (messaging network)
1. Listen for any matching offers (messaging network)
1. Validate them (colorlib + bitcoin client)
1. Sign and broadcast them (bitcoin client)
