Color module
============

The module needs to implement the following two functions:

- colorvalue(colordef, utxo) - returns the unspent color value of utxo (a tuple in the form (txhash, outputindex)) if it is of color colordef, or false if it is not.
- makeconversion(txspec, our, their) - returns a raw color conversion transaction according to txspec. The other two parameters are a patchy leftover and will soon be removed.

We are using a small patch over Alex's ngccc-server, which implements the required API calls. You can find it here:
https://github.com/israellevin/ngcccbase

It will be automatically fetched when you fetch the submodules, and you can install it with ```sudo python ./ngcccbase/setup.py install``` (you will need the package ```python-setuptools```). If you haven't done so yet, please go to the project's root and use ```git submodule init``` once, and than use ```git submodule update``` to update it.

The module runs ngccc-server automatically on startup, and implements the close function that shuts it down.

Note that ngccc-server is currently hardcoded to run in testnet mode.

Also note that if you do not have enough coins in your ngccc testnet wallet (the file ```testnet.wallet```) to pay fees, the ```makeconversion``` call will fail. We will get rid of this dependancy soon by adding the fees to the proposal.

Protip: you can install ngccc in a virtualenv, and change the name of the python executable in the Popen call in __init__.py to the python executable of your virtualenv. A similar trick might get you going if you want to get this running on Windows.
