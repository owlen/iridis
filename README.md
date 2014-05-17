Iridis
======

ColoredCoins implementation.

Framework for a swift and decentralized coloredcoins marketplace.

See https://groups.google.com/forum/#!tags/bitcoinx/Iridis

## Beware, here be pre-alpha code and ideas ##

As we are currently in a testing phase, we don't have any complete code to share. Nonetheless, instead of setting a date for publicly unveiling our code we have decided to start sharing everything right away - even the most rudimentary tests with hard-coded private keys and all.

## What are we trying to do? ##

Build a simple framework into which the different components required for healthy p2p coloredcoins commerce.

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

We are in the process of identifying and cataloguing all the different capabilities required for different types of players in a coloredcoins marketplace, and assigning them to separate components of the system, that interface with each other via JSON-RPC.

At any design point we prefer completeness over complexity, but at any implementation point we prefer modularity over completeness. This way we are trying to ensure a clear path of development with a safe way for other contributors to participate.

Here is a list of the components, and the capabilities they should provide.

- Color server:
    - Get color value of transaction
    - Create unsigned conversion transaction between different colors
- Message server:
    - Broadcast messages to the channel
    - Get messages from channel (this might become asynchronous one day, right now we just don't care)
- Bitcoin server:
    - Sign transaction
    - Broadcast transaction

This list is partial, of course, and very minimal. The color server, for example, does not have any issuance capabilities at the moment. Issuance is a big thing that involves money and contracts, and for now can be done manually.

With these three servers, a wide range of trading clients can be built. Specifically we are laying with thin color aware trading wallets, web wallets that offer browser based trading and automated market makers.

## What do we have? ##

The different components, which should be interchangeable, are held in this git repository as submodules, so you can mix and match and run whichever you like as well as develop your own.

Currently, you will find the following
- Color servers:
    - A fork of ChromaWallet with a patched ngccc-server
    - A fork of multibit which implements a simple color scheme (currently integrated with trading clients)
- Message servers:
    - A thin wrapper over bitmessage
- Bitcoin servers:
    - A thin wrapper over bitcoind (we are working on a bitcoinj version)
- Trading clients:
    - A python script with hard coded color definitions and UTXO lists that simulates trade - more a testing tool than an actual UI
    - A fork of multibit which implements a simple color scheme (currently integrated with color server)
    - A demo web app for very basic trading

## What can you do? ##

### prerequisites ###

```sh
sudo apt-get install bitcoind
sudo pip3 install jsonrpclib-pelix
```

### updated sub modules

From the repository's root directory, issue the following two commands:

```sh
git submodule init
git submodule update
```
### running

In the current branch, you can simply run `trader.py` which includes a small web server, and browse to [http://localhost:8000](http://localhost:8000) to run the demo web app.

This script activates the messaging layer and the coloring library, so make sure you followed the instructions in the readme files in the `message` and `color` directories.

Soon you will be able to check out other branches, like a market viewer branch with a web UI, a testscript branch, which has a test script instead of a web UI, a market maker branch, and the long awaited multibit branch, which isn't yet well integrated into our framework, so you will need to work harder to run it. Much fun ahead.
