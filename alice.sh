#!/bin/bash

source init.sh alice

# Colored input
clrin='{"txid": "420bb3b842d511f12d7b15a2e95b136194c2e5bfaac763a5effba5ccc3a8cdcc", "vout": 0}'

# Uncolored input (for fee)
btcin='{"txid": "420bb3b842d511f12d7b15a2e95b136194c2e5bfaac763a5effba5ccc3a8cdcc", "vout": 1}'

# Create multisig address from two pubkeys
apubk=0256b41e08bc562137bc9a405fa9b14e13afe5c49ff2b73ea0d9592e665ffde1d3
bpubk=0337a44e5843931a352bb1e7c01f14f2c1e5807ef9bf2d6a7076b624ca65d86b50
sig='["'$apubk'", "'$bpubk'"]'
addr="$($bitcoincmd createmultisig 2 "$sig" | grep -Pom1 "(?<=\"address\" : \")[^\"]*")"

# Colored output first, then change
txout='{"'$addr'": 0.00008392, "mgvtb4PBYSixPVh2KBpua2CDsENAKStC1x": 0.67881608}'

# Create transaction
dang="$($bitcoincmd createrawtransaction "[$clrin, $btcin]" "$txout")"

# Sign it
dang="$($bitcoincmd signrawtransaction "$dang" | grep -Pom1 "(?<=\"hex\" : \")[^\"]*")"
$bitcoincmd signrawtransaction "$dang"

#$bitcoincmd decoderawtransaction $dang

exit 5

# Send it
$bitcoincmd sendrawtransaction "$dang"

exit 0
