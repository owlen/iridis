Message module
==============

The module needs to implement the following two functions:

- send(subject, body) => return the bitmessage confirmation of the send
- receive() => return a list of new messages

We are using pyBitmessage in daemon mode as an XML-RPC server.

You need to manually copy the bitmessage config file, keys.dat, from this directory to the bitmessage config directory, overriding your current settings. To find out which directory that is, you can run the following command from the current directory:

```sh
PYTHONPATH=./PyBitmessage/src/ python -c 'from shared import lookupAppdataFolder as f; print(f());'
```

The module runs it automatically when you run the trader.py script from the project's root, with the keys.dat configuration file and implements the close function that shuts it down.

Protip: If you want to run multiple instances of PyBitmessage with different settings, you can override the lookupAppdataFolder function if PyBitmessage/src/shared.py line 132 and return any directory of your choosing.
