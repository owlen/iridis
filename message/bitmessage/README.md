bitmessage based message server
===============================

This is a thin wrapper around pyBitmessage which implements send and receive. The keys for the channel, a test key and some required settings for pyBitmessage are all in the keys.dat file.

If you want to run multiple instances of PyBitmessage with different settings, you can override the lookupAppdataFolder function if PyBitmessage/src/shared.py line 132 and return any directory of your choosing.

To run it just run PyBitmessage/src/bitmessagemain.py
