#!/bin/bash

bitcoincmd="bitcoind.easy --datadir="
clean () {
    ${bitcoincmd}alice stop
    ${bitcoincmd}bob stop
}

# Run local testnet
pgrep -f "bitcoin" &&
echo 'found something that looks like a running bitcoin client, not taking any chances' > "$errlog" &&
exit 1

${bitcoincmd}alice
${bitcoincmd}bob
exec 6>&1 7>&2 1>/dev/null 2>/dev/null
while :; do
    ${bitcoincmd}alice getinfo && ${bitcoincmd}bob getinfo && break
done
exec 1>&6 2>&7

# Simplistic JSON reader
# TODO: Get the bitcoincmd into it instead of repeating it all the time
getjsval() { grep -Pom1 "(?<=\"$1\" : \")[^\"]*"; }

# Get alice's details: address, pubkey, privkey and an unspent transaction
aaddr="$(${bitcoincmd}alice getaddressesbyaccount '' | grep -Pom 1 '(?<=")[^",]*')"
apubk="$(${bitcoincmd}alice validateaddress $aaddr | getjsval pubkey)"
apriv="$(${bitcoincmd}alice dumpprivkey $aaddr)"
aintx="$(${bitcoincmd}alice listunspent | getjsval txid)"

# Get bob's details: address, pubkey, privkey and an unspent transaction
baddr="$(${bitcoincmd}bob getaddressesbyaccount '' | grep -Pom 1 '(?<=")[^",]*')"
bpubk="$(${bitcoincmd}bob validateaddress $baddr | getjsval pubkey)"
bpriv="$(${bitcoincmd}bob dumpprivkey $baddr)"
# bob is broke
#bintx="$(${bitcoincmd}bob listunspent | getjsval txid)"

# alice creates a danglage transaction for her and bob
sig="[\"$apubk\",\"$bpubk\"]"
sig="$(${bitcoincmd}alice createmultisig 2 "$sig")"
addr="$(echo "$sig" | getjsval address)"
txin="[{\"txid\": \"$aintx\", \"vout\": 0}]"
txout="{\"$addr\": 49}"
dang="$(${bitcoincmd}alice createrawtransaction "$txin" "$txout")"
dang="$(${bitcoincmd}alice signrawtransaction $dang | getjsval hex)"

# And, for starters, a transaction that sends the danglage to bob
redeem="$(echo "$sig" | getjsval redeemScript)"
# What an ugly hack - we need a less simplistic JSON reader
pubk="$(${bitcoincmd}alice decoderawtransaction "$dang" | tail -n 20 | getjsval hex)"
txin="$(${bitcoincmd}alice decoderawtransaction "$dang" | getjsval txid)"
txin="[{\"txid\": \"$txin\",\"vout\": 0, \"scriptPubKey\": \"$pubk\", \"redeemScript\": \"$redeem\"}]"
txout="{\"$baddr\": 48}"
cashout="$(${bitcoincmd}alice createrawtransaction "$txin" "$txout")"

# alice signs with her key
key="[\"$apriv\"]"
cashout="$(${bitcoincmd}alice signrawtransaction "$cashout" "$txin" "$key" | getjsval hex)"

# and bob signs with his
key="[\"$bpriv\"]"
cashout="$(${bitcoincmd}bob signrawtransaction "$cashout" "$txin" "$key" | getjsval hex)"

# bob checks his balance and block count
balance="$(${bitcoincmd}bob getbalance)"
blocks="$(${bitcoincmd}bob getblockcount)"
echo "bob has $balance in block $blocks"

# alice broadcasts both transactions (she is the only one with broadcasting power in our local testnet)
${bitcoincmd}alice sendrawtransaction "$dang"
${bitcoincmd}alice sendrawtransaction "$cashout"
sleep 10

# Now we wait a block and see if bob's balance increased
while [ "$blocks" = "$(${bitcoincmd}bob getblockcount)" ]; do :; done
balance="$(${bitcoincmd}bob getbalance)"
blocks="$(${bitcoincmd}bob getblockcount)"
echo "bob has $balance in block $blocks"

clean
exit 0
