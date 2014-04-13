ematadoro
=========

Framework for a swift and decentralized coloredcoins marketplace.

See https://groups.google.com/d/msg/bitcoinx/o9LYhbomuIE/usOCm2JVWxcJ

## Beware, here be pre-alpha code and ideas ##

As we are currently in a testing phase, we don't have any complete code to share. Nonetheless, instead of setting a date for publicly unveiling our code we have decided to start sharing everything right away - even the most rudimentary tests with hard-coded private keys and all.

## What are we trying to do? ##

Build a simple framework into which the different components required for healthy p2p coloredcoins commerce.

At any design point we prefer completeness over complexity, but at any implementation point we prefer modularity over completeness. This way we are trying to ensure a clear path of development with a safe way for other contributors to participate.

The most naive implementation for a trader should do the following:

1. Receive user interests from UI
1. Broadcast them to the marketplace as propositions
1. Listen for any matching propositions in the marketplace
    1. Validate them
    1. Construct matching atomic transactions
    1. Partially sign them
    1. Broadcast them to the marketplace
1. Listen for any matching partially signed transactions in the marketplace
    1. Validate them
    1. Sign them
    1. Broadcast them to the bitcoin network

## What do we need? ##

We are in the process of identifying and cataloguing all the different capabilities required for different types of players in a coloredcoins marketplace, and assigning them to separate components of the system. Here is a list of the components, and the capabilities they should provide.

- bitcoin client - we are currently using bitcoinj, with thin clients in mind, but some tests may require bitcoind (hint: using [freewil](https://github.com/freewil)'s easy mining fork on an internal bitcoin net can come very handy when testing). It provides the following:
    - Validate transactions
    - Sign transactions
    - Broadcast transactions
- color server - we are trying to use ngccc-server here, but until ngcccbase becomes stable we also create a "fake" version which for testing.
    - Test outputs against known colors
    - Create unsigned conversion transactions between different colors
- pseudonymous p2p message server - we are currently using bitmessage as the underlying technology, not because we are convinced it's the right technology, but because it works. Replacing it should be trivial.
    - Broadcast messages to the channel
    - Get messages from channel (this might become asynchronous one day, right now we just don't care)
- Interface to a financial something or other
    - Market maker
    - Hedging

This list is partial, of course, and very minimal. Our color lib, for example, does not have any issuance capabilities at the moment. Issuance is a big thing that involves money and contracts, and for now can be done manually.

## What do we have? ##

We chose JSON/RPC as the interface between the components, so we currently have thin python3 wrappers that act as RPC servers on top of whatever component we use.

### messages.py ###

Connects to an instance of [pybitmessage](https://github.com/Bitmessage/PyBitmessage) running with the supplied keys.dat (it is possible to patch the function lookupAppdataFolder in shared.py to support multiple instances running with different dat files, if you want to test multiple users) and provides the following functions on port 6711:

- send(subject, message) -> success of broadcasting message to the network
- receive() -> list of new messages

### color.py ###

Connects to nothing at all ATM, and provides these two fake functions:

- getoutputvalue(color, output) -> amount
- makeconversion(color, amount1, key, outputs, amount2) -> a tx that transfers amount of color (signed with key) to the address of outputs, and amount2 from outputs to key's address (unsigned)

Note that this is just a placeholder for testing. We are working on bringing ngccc-server.py to solidly provide this functionality, and on an independent bitcoinj based implementation - with thin wallets in mind.

### trader.py ###

This is currently a simple test script for the messaging server, and as it will mature (and split into "alice" and "bob" parts) it will demonstrate how the different components can be used.
