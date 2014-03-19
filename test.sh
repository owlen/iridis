#!/bin/bash

# Run local testnet
bitcoincmd="bitcoind --datadir="
clean () {
    ${bitcoincmd}alice stop
    ${bitcoincmd}bob stop
}
#trap clean EXIT
#
#pgrep -f "bitcoin" &&
#echo 'found something that looks like a running bitcoin client, not taking any chances' &&
#exit 1
#
${bitcoincmd}alice
${bitcoincmd}bob
exec 6>&1 7>&2 1>/dev/null 2>/dev/null
while :; do
    ${bitcoincmd}alice getinfo && ${bitcoincmd}bob getinfo && break
done
exec 1>&6 2>&7

# Primitive dispatcher + parser for bitcoind RPC calls
getval() {
    # It's easy when there is no JSON to parse
    if [ 'nojson' = "$1" ]; then
        local usr="$2"
        shift 2
        # Just make sure you quote complex commands
        if [ "$3" ]; then
            ${bitcoincmd}$usr "$1" "$2" "$3"
        else
            ${bitcoincmd}$usr $@
        fi
    else
        # Check if we want the last result - otherwise we go with first
        # TODO: Should I move nojson and last flags to end and use "${@:0:$#}"
        # and "${@: -1}"? It's less code, but not too readable and very bashocentric.
        if [ 'last' = "$1" ]; then
            local last=true
            shift
        fi
        local usr="$1"
        local cmd="$2"
        # This is a special case where bitcoind returns an array instead of JSON
        if [ 'getaddressesbyaccount' = "$cmd" ]; then
            ${bitcoincmd}$usr $cmd '' | grep -Pom1 '(?<=")[^\",]*'
        else
            local key="$3"
            if [ 'true' = "$last" ]; then
                ${bitcoincmd}$usr $cmd | grep -Po "(?<=\"$key\" : \")[^\"]*" | tail -n1
            else
                ${bitcoincmd}$usr $cmd | grep -Pom1 "(?<=\"$key\" : \")[^\"]*"
            fi
        fi
    fi
}

# Get alice's details: address, pubkey, privkey and an unspent transaction
aaddr="$(getval alice getaddressesbyaccount)"
apriv="$(getval nojson alice dumpprivkey $aaddr)"
apubk="$(getval alice "validateaddress $aaddr" pubkey)"
aintx="$(getval alice listunspent txid)"

# Get bob's details: address, pubkey, privkey and an unspent transaction
baddr="$(getval bob getaddressesbyaccount)"
bpriv="$(getval nojson bob dumpprivkey $baddr)"
bpubk="$(getval bob "validateaddress $baddr" pubkey)"
# bob is probably broke
#bintx="$(getval bob listunspent txid)"

# alice creates a danglage transaction for her and bob
sig="[\"$apubk\",\"$bpubk\"]"
addr="$(getval alice "createmultisig 2 $sig" address)"
txin="[{\"txid\": \"$aintx\", \"vout\": 0}]"
txout="{\"$addr\": 49}"
dang="$(getval nojson alice createrawtransaction "$txin" "$txout")"
dang="$(getval alice "signrawtransaction $dang" hex)"

# And, for starters, a transaction that sends the danglage to bob
redeem="$(getval alice "createmultisig 2 $sig" redeemScript)"
pubk="$(getval last alice "decoderawtransaction $dang" hex)"
txin="$(getval alice "decoderawtransaction $dang" txid)"
txin="[{\"txid\":\"$txin\",\"vout\":0,\"scriptPubKey\":\"$pubk\",\"redeemScript\":\"$redeem\"}]"
txout="{\"$baddr\":48}"
cashout="$(getval nojson alice createrawtransaction "$txin" "$txout")"
echo so far

# alice signs with her key
key="[\"$apriv\"]"
cashout="$(getval alice "signrawtransaction $cashout $txin $key" hex)"

# and bob signs with his
key="[\"$bpriv\"]"
cashout="$(getval bob "signrawtransaction $cashout $txin $key" hex)"

# bob checks his balance
balance="$(getval nojson bob getbalance)"
blocks="$(getval nojson bob getblockcount)"
echo "Block $blocks: bob has $balance BTC"

# alice broadcasts both transactions (she is the only one with broadcasting power in our local testnet)
echo Broadcasting transactions
${bitcoincmd}alice sendrawtransaction "$dang"
${bitcoincmd}alice sendrawtransaction "$cashout"

# Now we wait for bob's balance to increase
echo Waiting for confirmation
while [ "$balance" = "$(getval nojson bob getbalance)" ]; do :; done
balance="$(getval nojson bob getbalance)"
blocks="$(getval nojson bob getblockcount)"
echo "Block $blocks: bob has $balance BTC"

exit 0
