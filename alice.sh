#!/bin/bash

source init.sh alice

# Colored input
clrin='{"txid": "7da1bbd84942b902d0fb0318f1541b8591ff754899ce090a521caa847f7ae5b8", "vout": 0}'

# Uncolored input (for fee)
btcin='{"txid": "7da1bbd84942b902d0fb0318f1541b8591ff754899ce090a521caa847f7ae5b8", "vout": 1}'

# Create multisig address from two pubkeys
apubk=0256b41e08bc562137bc9a405fa9b14e13afe5c49ff2b73ea0d9592e665ffde1d3
epubk=0337a44e5843931a352bb1e7c01f14f2c1e5807ef9bf2d6a7076b624ca65d86b50
msig='["'$apubk'", "'$epubk'"]'
msig="$($bitcoincmd createmultisig 2 "$msig")"
msaddr="$(echo "$msig" | grep -Pom1 "(?<=\"address\" : \")[^\"]*")"
redeem="$(echo "$msig" | grep -Pom1 "(?<=\"redeemScript\" : \")[^\"]*")"

# Colored output first, then change
txout='{"'$msaddr'": 0.000001, "miHAzgUWtaypUMtA7cbV1QUoT7rPu2XXLH": 0.49918}'

# Create danglage
dang="$($bitcoincmd createrawtransaction "[$clrin, $btcin]" "$txout")"

# Sign it
dang="$($bitcoincmd signrawtransaction "$dang" | grep -Pom1 "(?<=\"hex\" : \")[^\"]*")"

dang=0100000002b8e57a7f84aa1c520a09ce994875ff91851b54f11803fbd002b94249d8bba17d000000008a47304402204d82e5f4d012c1857890d5f368979a2608d31da43237140602749858e455d1b202205b9f72fe2ab5cc3aa4f345e95b32d2c1a8d253b4c66c6d6a0c5b2e29375ffac0014104e2bde51ecbedf53ac73650a6be4cfa7b833557a4c40f46ca785def18dfbfb2b8c3e0b00f3e9c1f03b494c806985023c1c68fe1eb0462958dadd60e3c7300b6ffffffffffb8e57a7f84aa1c520a09ce994875ff91851b54f11803fbd002b94249d8bba17d010000008b4830450221008d66e00342e4b66852f88ae7b6f5daff04e484fedc0fdd16a9f61524f4f465d4022070e1a9c99e087c7c549af9f878a7189fd27fbb05d5106c9c4b68a0880f303121014104b337154cbe51ca34f816898ff1b472d70f2fbd3a6f8418adc9cdd7485a75c1df338af40883a9268d1eed87c4ef4f0017bd5c566c9f22f9bc6dde34a2911e96fdffffffff02640000000000000017a9140d3142623647607e82360aca2f5e119b8a86d9ac8730b0f902000000001976a9141e4d27dc6311f1ae9f0d758d15bf820d7c6bc0a488ac00000000

# Get data
$bitcoincmd decoderawtransaction "$dang"
(read -n 1 -p 'hit y to continue' q; echo; [ y = "$q" ]) || exit 0
txid=87499bc1e51a04562c5f26c814299014b0903c1e2f0971930bcdd5c45f619245
clrscrpubk=a9140d3142623647607e82360aca2f5e119b8a86d9ac87
btcscrpubk=76a9141e4d27dc6311f1ae9f0d758d15bf820d7c6bc0a488ac

# Refund inputs
clrin='{"txid": "'$txid'", "vout": 0, "scriptPubKey": "'$clrscrpubk'", "redeemScript": "'$redeem'"}'
btcin='{"txid": "'$txid'", "vout": 1, "scriptPubKey": "'$btcscrpubk'"}'

# Refund outputs
txout='{"msWk1KZ36K4qZKxyctKjFEogBtJwrS64vB": 0.000002, "miHAzgUWtaypUMtA7cbV1QUoT7rPu2XXLH": 0.569009}'

# Create refund
refund="$($bitcoincmd createrawtransaction "[$clrin, $btcin]" "$txout")"

echo $bitcoincmd signrawtransaction "$refund" "[$clrin]"
(read -n 1 -p 'hit y to continue' q; echo; [ y = "$q" ]) || exit 0

refund=01000000024592615fc4d5cd0b9371092f1e3c90b014902914c8265f2c56041ae5c19b498700000000910047304402206f790145339ea656f49c65f5df5dace2a8c4c6e407f37b2ffc03926afeb0b1df022013595c873dc4df03142f13069286ebffa85f9c96634165effc56e76d8a5c2345014752210256b41e08bc562137bc9a405fa9b14e13afe5c49ff2b73ea0d9592e665ffde1d3210337a44e5843931a352bb1e7c01f14f2c1e5807ef9bf2d6a7076b624ca65d86b5052aeffffffff4592615fc4d5cd0b9371092f1e3c90b014902914c8265f2c56041ae5c19b49870100000000ffffffff02c8000000000000001976a91483974060d094b6598ebec0ba26daf28aca0f288988ac243d6403000000001976a9141e4d27dc6311f1ae9f0d758d15bf820d7c6bc0a488ac00000000

$bitcoincmd decoderawtransaction "$refund"
exit 4
echo $refund | wc

# Partially sign color input
clrprvk='["92sBnPm59x5Wb2PTpzQAuwb657eDHs5owyFcPP18ywo4f9tzXQv"]'
refund="$($bitcoincmd signrawtransaction "$refund" "[$clrin]" "$clrprvk" | grep -Pom1 "(?<=\"hex\" : \")[^\"]*")"
echo $refund | wc

# Fully sign BTC input
btcprvk='["9335ad9S8gwVadH7jjkahP5ChH7ukevxKG9EDW27gr2Hq2aXcVC"]'
refund="$($bitcoincmd signrawtransaction "$refund" "[$btcin]" "$btcprvk" | grep -Pom1 "(?<=\"hex\" : \")[^\"]*")"
echo $refund | wc

# Send it
$bitcoincmd sendrawtransaction "$dang"
read -p 'hit enter to refund'
$bitcoincmd sendrawtransaction "$refund"

exit 0
