#!/bin/bash

source init.sh alice

# Colored input
clrin='{"txid": "944c8f9d406e4237435411a8058394cee24d0bf6f17465ded3e43ead7280ac31", "vout": 0, "scriptPubKey" : "76a9141eabce1c4d99df2eb5a0a56c57f36d08e9250a9a88ac"}'

# Uncolored input (for fee)
btcin='{"txid": "944c8f9d406e4237435411a8058394cee24d0bf6f17465ded3e43ead7280ac31", "vout": 1, "scriptPubKey" : "76a9141e4d27dc6311f1ae9f0d758d15bf820d7c6bc0a488ac"}'

# Create multisig address from two pubkeys
pubAclr=044d58335abdd1ddffae6cf6287e526fca43f414284e8da7bf96714d5a50100aeaef51618741f0ad16fc872e9d890bf48d11c2093cc71fd50afb8471ef6f0dc27a
pubEall=02181af67ac9c37284f995f37a19c0b2236f5ce4e099ce188951791e853c170648
msig='["'$pubAclr'", "'$pubEall'"]'
msig="$($bitcoincmd createmultisig 2 "$msig")"
msaddr="$(echo "$msig" | grep -Pom1 "(?<=\"address\" : \")[^\"]*")"
redeem="$(echo "$msig" | grep -Pom1 "(?<=\"redeemScript\" : \")[^\"]*")"

# Colored output first, then change
txout='{"'$msaddr'": 0.000001, "miHAzgUWtaypUMtA7cbV1QUoT7rPu2XXLH": 0.099898}'

# Create danglage
dang="$($bitcoincmd createrawtransaction "[$clrin, $btcin]" "$txout")"

# Sign it
prvAclr='["93JNn11rTDS98h942XH5kAPCazBTePm6Ex4bfSQKZatR8uYd5yL"]'
prvAbtc='["9335ad9S8gwVadH7jjkahP5ChH7ukevxKG9EDW27gr2Hq2aXcVC"]'
dang="$($bitcoincmd signrawtransaction "$dang" "[$clrin, $btcin]" "$prvAclr" | grep -Pom1 "(?<=\"hex\" : \")[^\"]*")"
$bitcoincmd signrawtransaction "$dang" "[$clrin, $btcin]" "$prvAbtc"
dang="$($bitcoincmd signrawtransaction "$dang" "[$clrin, $btcin]" "$prvAbtc" | grep -Pom1 "(?<=\"hex\" : \")[^\"]*")"

# Get data
#(read -n 1 -p 'hit y to continue' q; echo; [ y = "$q" ]) || exit 0
dang=010000000231ac8072ad3ee4d3de6574f1f60b4de2ce948305a811544337426e409d8f4c94000000008b48304502206b593c7d8fa3f9265ae4054d04aa5ca0f0dc2135dec67e63bc87f6c94b4cf117022100e217d1485f03c63d908adb80fb8bedbff0a9598c0c561e67a27780334035e6ec0141044d58335abdd1ddffae6cf6287e526fca43f414284e8da7bf96714d5a50100aeaef51618741f0ad16fc872e9d890bf48d11c2093cc71fd50afb8471ef6f0dc27affffffff31ac8072ad3ee4d3de6574f1f60b4de2ce948305a811544337426e409d8f4c94010000008c493046022100ed35aea926bef99115da642a0d9e8a6035843e6dcc2ee39534c26e646ed74624022100aef59b518151ac9cc312da0725d093e66ec786a94aa0d88566aa0d7694ffe660014104b337154cbe51ca34f816898ff1b472d70f2fbd3a6f8418adc9cdd7485a75c1df338af40883a9268d1eed87c4ef4f0017bd5c566c9f22f9bc6dde34a2911e96fdffffffff02640000000000000017a914b949361b53d44a30faf6b593e84eecde1b9a4f1d87a86e9800000000001976a9141e4d27dc6311f1ae9f0d758d15bf820d7c6bc0a488ac00000000
#$bitcoincmd decoderawtransaction "$dang"
#(read -n 1 -p 'hit y to continue' q; echo; [ y = "$q" ]) || exit 0
txid=bd5f71b614a0366c39315fc3a3305bd6f4550dbd676df7fbe52385ada37ec67c
clrscrpubk=a914f41caed95bc214f731bb572e8867ddce8c13a26387
btcscrpubk=76a9141e4d27dc6311f1ae9f0d758d15bf820d7c6bc0a488ac

# Refund inputs
clrin='{"txid": "'$txid'", "vout": 0, "scriptPubKey": "'$clrscrpubk'", "redeemScript": "'$redeem'"}'
btcin='{"txid": "'$txid'", "vout": 1, "scriptPubKey": "'$btcscrpubk'"}'

# Refund outputs
txout='{"miK8P39kePAQVXfrm12PkCusvqsu49VBuu": 0.000001, "miHAzgUWtaypUMtA7cbV1QUoT7rPu2XXLH": 0.099897}'

# Create refund
refund="$($bitcoincmd createrawtransaction "[$clrin, $btcin]" "$txout")"

# Sign refund
echo '!!!'
$bitcoincmd decoderawtransaction "$refund"
echo $refund | wc
refund="$($bitcoincmd signrawtransaction "$refund" "[$clrin, $btcin]" "$prvAbtc" | grep -Pom1 "(?<=\"hex\" : \")[^\"]*")"
$bitcoincmd decoderawtransaction "$refund"
echo $refund | wc
refund="$($bitcoincmd signrawtransaction "$refund" "[$clrin, $btcin]" "$prvAclr" | grep -Pom1 "(?<=\"hex\" : \")[^\"]*")"
$bitcoincmd decoderawtransaction "$refund"
echo $refund | wc
echo '!!!'

prvEall='["cVs73nsBTF8nLeGphmxCumXp1wSFCjFXS6vGsH2venqr3u9Ct8Pw"]'
$bitcoincmd signrawtransaction "$refund" "[$clrin, $btcin]" "$prvEall"
#$bitcoincmd decoderawtransaction "$refund"
#(read -n 1 -p 'hit y to continue' q; echo; [ y = "$q" ]) || exit 0
exit 5





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



  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0# Raw transaction API example work-through
# Send coins to a 2-of-3 multisig, then spend them.
#
# For this example, I'm using these three keypairs (public/private)
# 0491bba2510912a5bd37da1fb5b1673010e43d2c6d812c514e91bfa9f2eb129e1c183329db55bd868e209aac2fbc02cb33d98fe74bf23f0c235d6126b1d8334f86 / 5JaTXbAUmfPYZFRwrYaALK48fN6sFJp4rHqq2QSXs8ucfpE4yQU
# 04865c40293a680cb9c020e7b1e106d8c1916d3cef99aa431a56d253e69256dac09ef122b1a986818a7cb624532f062c1d1f8722084861c5c3291ccffef4ec6874 / 5Jb7fCeh1Wtm4yBBg3q3XbT6B525i17kVhy3vMC9AqfR6FH2qGk
# 048d2455d2403e08708fc1f556002f1b6cd83f992d085097f9974ab08a28838f07896fbab08f39495e15fa6fad6edbfb1e754e35fa1c7844c41f322a1863d46213 / 5JFjmGo5Fww9p8gvx48qBYDJNAzR9pmH5S389axMtDyPT8ddqmw

# First: combine the three keys into a multisig address:
./bitcoind createmultisig 2 '["0491bba2510912a5bd37da1fb5b1673010e43d2c6d812c514e91bfa9f2eb129e1c183329db55bd868e209aac2fbc02cb33d98fe74bf23f0c235d6126b1d8334f86","04865c40293a680cb9c020e7b1e106d8c1916d3cef99aa431a56d253e69256dac09ef122b1a986818a7cb624532f062c1d1f8722084861c5c3291ccffef4ec6874","048d2455d2403e08708fc1f556002f1b6cd83f992d085097f9974ab08a28838f07896fbab08f39495e15fa6fad6edbfb1e754e35fa1c7844c41f322a1863d46213"]'

{
    "address" : "3QJmV3qfvL9SuYo34YihAf3sRCW3qSinyC",
    "redeemScript" : "52410491bba2510912a5bd37da1fb5b1673010e43d2c6d812c514e91bfa9f2eb129e1c183329db55bd868e209aac2fbc02cb33d98fe74bf23f0c235d6126b1d8334f864104865c40293a680cb9c020e7b1e106d8c1916d3cef99aa431a56d253e69256dac09ef122b1a986818a7cb624532f062c1d1f8722084861c5c3291ccffef4ec687441048d2455d2403e08708fc1f556002f1b6cd83f992d085097f9974ab08a28838f07896fbab08f39495e15fa6fad6edbfb1e754e35fa1c7844c41f322a1863d4621353ae"
}

# Next, create a transaction to send funds into that multisig. Transaction d6f72... is
# an unspent transaction in my wallet (which I got from the 'listunspent' RPC call):
./bitcoind createrawtransaction '[{"txid" : "d6f72aab8ff86ff6289842a0424319bf2ddba85dc7c52757912297f948286389","vout":0}]' '{"3QJmV3qfvL9SuYo34YihAf3sRCW3qSinyC":0.01}'

010000000189632848f99722915727c5c75da8db2dbf194342a0429828f66ff88fab2af7d60000000000ffffffff0140420f000000000017a914f815b036d9bbbce5e9f2a00abd1bf3dc91e955108700000000

# ... and sign it:
./bitcoind signrawtransaction 010000000189632848f99722915727c5c75da8db2dbf194342a0429828f66ff88fab2af7d60000000000ffffffff0140420f000000000017a914f815b036d9bbbce5e9f2a00abd1bf3dc91e955108700000000

{
    "hex" : "010000000189632848f99722915727c5c75da8db2dbf194342a0429828f66ff88fab2af7d6000000008b483045022100abbc8a73fe2054480bda3f3281da2d0c51e2841391abd4c09f4f908a2034c18d02205bc9e4d68eafb918f3e9662338647a4419c0de1a650ab8983f1d216e2a31d8e30141046f55d7adeff6011c7eac294fe540c57830be80e9355c83869c9260a4b8bf4767a66bacbd70b804dc63d5beeb14180292ad7f3b083372b1d02d7a37dd97ff5c9effffffff0140420f000000000017a914f815b036d9bbbce5e9f2a00abd1bf3dc91e955108700000000",
    "complete" : true
}

# Now, create a transaction that will spend that multisig transaction. First, I need the txid
# of the transaction I just created, so:
./bitcoind decoderawtransaction 010000000189632848f99722915727c5c75da8db2dbf194342a0429828f66ff88fab2af7d6000000008b483045022100abbc8a73fe2054480bda3f3281da2d0c51e2841391abd4c09f4f908a2034c18d02205bc9e4d68eafb918f3e9662338647a4419c0de1a650ab8983f1d216e2a31d8e30141046f55d7adeff6011c7eac294fe540c57830be80e9355c83869c9260a4b8bf4767a66bacbd70b804dc63d5beeb14180292ad7f3b083372b1d02d7a37dd97ff5c9effffffff0140420f000000000017a914f815b036d9bbbce5e9f2a00abd1bf3dc91e955108700000000

{
    "txid" : "3c9018e8d5615c306d72397f8f5eef44308c98fb576a88e030c25456b4f3a7ac",
    ... etc, rest omitted to make this shorter
}

# Create the spend-from-multisig transaction. Since the fund-the-multisig transaction
# hasn't been sent yet, I need to give txid, scriptPubKey and redeemScript:
./bitcoind createrawtransaction '[{"txid":"3c9018e8d5615c306d72397f8f5eef44308c98fb576a88e030c25456b4f3a7ac","vout":0,"scriptPubKey":"a914f815b036d9bbbce5e9f2a00abd1bf3dc91e9551087","redeemScript":"52410491bba2510912a5bd37da1fb5b1673010e43d2c6d812c514e91bfa9f2eb129e1c183329db55bd868e209aac2fbc02cb33d98fe74bf23f0c235d6126b1d8334f864104865c40293a680cb9c020e7b1e106d8c1916d3cef99aa431a56d253e69256dac09ef122b1a986818a7cb624532f062c1d1f8722084861c5c3291ccffef4ec687441048d2455d2403e08708fc1f556002f1b6cd83f992d085097f9974ab08a28838f07896fbab08f39495e15fa6fad6edbfb1e754e35fa1c7844c41f322a1863d4621353ae"}]' '{"1GtpSrGhRGY5kkrNz4RykoqRQoJuG2L6DS":0.01}'

0100000001aca7f3b45654c230e0886a57fb988c3044ef5e8f7f39726d305c61d5e818903c0000000000ffffffff0140420f00000000001976a914ae56b4db13554d321c402db3961187aed1bbed5b88ac00000000

# ... Now I can partially sign it using one private key:
./bitcoind signrawtransaction '0100000001aca7f3b45654c230e0886a57fb988c3044ef5e8f7f39726d305c61d5e818903c0000000000ffffffff0140420f00000000001976a914ae56b4db13554d321c402db3961187aed1bbed5b88ac00000000' '[{"txid":"3c9018e8d5615c306d72397f8f5eef44308c98fb576a88e030c25456b4f3a7ac","vout":0,"scriptPubKey":"a914f815b036d9bbbce5e9f2a00abd1bf3dc91e9551087","redeemScript":"52410491bba2510912a5bd37da1fb5b1673010e43d2c6d812c514e91bfa9f2eb129e1c183329db55bd868e209aac2fbc02cb33d98fe74bf23f0c235d6126b1d8334f864104865c40293a680cb9c020e7b1e106d8c1916d3cef99aa431a56d253e69256dac09ef122b1a986818a7cb624532f062c1d1f8722084861c5c3291ccffef4ec687441048d2455d2403e08708fc1f556002f1b6cd83f992d085097f9974ab08a28838f07896fbab08f39495e15fa6fad6edbfb1e754e35fa1c7844c41f322a1863d4621353ae"}]' '["5JaTXbAUmfPYZFRwrYaALK48fN6sFJp4rHqq2QSXs8ucfpE4yQU"]'

{
    "hex" : "0100000001aca7f3b45654c230e0886a57fb988c3044ef5e8f7f39726d305c61d5e818903c00000000fd15010048304502200187af928e9d155c4b1ac9c1c9118153239aba76774f775d7c1f9c3e106ff33c0221008822b0f658edec22274d0b6ae9de10ebf2da06b1bbdaaba4e50eb078f39e3d78014cc952410491bba2510912a5bd37da1fb5b1673010e43d2c6d812c514e91bfa9f2eb129e1c183329db55bd868e209aac2fbc02cb33d98fe74bf23f0c235d6126b1d8334f864104865c40293a680cb9c020e7b1e106d8c1916d3cef99aa431a56d253e69256dac09ef122b1a986818a7cb624532f062c1d1f8722084861c5c3291ccffef4ec687441048d2455d2403e08708fc1f556002f1b6cd83f992d085097f9974ab08a28838f07896fbab08f39495e15fa6fad6edbfb1e754e35fa1c7844c41f322a1863d4621353aeffffffff0140420f00000000001976a914ae56b4db13554d321c402db3961187aed1bbed5b88ac00000000",
    "complete" : false
}

# ... and then take the "hex" from that and complete the 2-of-3 signatures using one of
# the other public keys (note the "hex" result getting longer):
./bitcoind signrawtransaction '0100000001aca7f3b45654c230e0886a57fb988c3044ef5e8f7f39726d305c61d5e818903c00000000fd15010048304502200187af928e9d155c4b1ac9c1c9118153239aba76774f775d7c1f9c3e106ff33c0221008822b0f658edec22274d0b6ae9de10ebf2da06b1bbdaaba4e50eb078f39e3d78014cc952410491bba2510912a5bd37da1fb5b1673010e43d2c6d812c514e91bfa9f2eb129e1c183329db55bd868e209aac2fbc02cb33d98fe74bf23f0c235d6126b1d8334f864104865c40293a680cb9c020e7b1e106d8c1916d3cef99aa431a56d253e69256dac09ef122b1a986818a7cb624532f062c1d1f8722084861c5c3291ccffef4ec687441048d2455d2403e08708fc1f556002f1b6cd83f992d085097f9974ab08a28838f07896fbab08f39495e15fa6fad6edbfb1e754e35fa1c7844c41f322a1863d4621353aeffffffff0140420f00000000001976a914ae56b4db13554d321c402db3961187aed1bbed5b88ac00000000' '[{"txid":"3c9018e8d5615c306d72397f8f5eef44308c98fb576a88e030c25456b4f3a7ac","vout":0,"scriptPubKey":"a914f815b036d9bbbce5e9f2a00abd1bf3dc91e9551087","redeemScript":"52410491bba2510912a5bd37da1fb5b1673010e43d2c6d812c514e91bfa9f2eb129e1c183329db55bd868e209aac2fbc02cb33d98fe74bf23f0c235d6126b1d8334f864104865c40293a680cb9c020e7b1e106d8c1916d3cef99aa431a56d253e69256dac09ef122b1a986818a7cb624532f062c1d1f8722084861c5c3291ccffef4ec687441048d2455d2403e08708fc1f556002f1b6cd83f992d085097f9974ab08a28838f07896fbab08f39495e15fa6fad6edbfb1e754e35fa1c7844c41f322a1863d4621353ae"}]' '["5JFjmGo5Fww9p8gvx48qBYDJNAzR9pmH5S389axMtDyPT8ddqmw"]'

{
    "hex" : "0100000001aca7f3b45654c230e0886a57fb988c3044ef5e8f7f39726d305c61d5e818903c00000000fd5d010048304502200187af928e9d155c4b1ac9c1c9118153239aba76774f775d7c1f9c3e106ff33c0221008822b0f658edec22274d0b6ae9de10ebf2da06b1bbdaaba4e50eb078f39e3d78014730440220795f0f4f5941a77ae032ecb9e33753788d7eb5cb0c78d805575d6b00a1d9bfed02203e1f4ad100 10443    0 10443    0     0  12158      0 --:--:-- --:--:-- --:--:-- 12157
9332d1416ae01e27038e945bc9db59c732728a383a6f1ed2fb99da7a4014cc952410491bba2510912a5bd37da1fb5b1673010e43d2c6d812c514e91bfa9f2eb129e1c183329db55bd868e209aac2fbc02cb33d98fe74bf23f0c235d6126b1d8334f864104865c40293a680cb9c020e7b1e106d8c1916d3cef99aa431a56d253e69256dac09ef122b1a986818a7cb624532f062c1d1f8722084861c5c3291ccffef4ec687441048d2455d2403e08708fc1f556002f1b6cd83f992d085097f9974ab08a28838f07896fbab08f39495e15fa6fad6edbfb1e754e35fa1c7844c41f322a1863d4621353aeffffffff0140420f00000000001976a914ae56b4db13554d321c402db3961187aed1bbed5b88ac00000000",
    "complete" : true
}

# And I can send the funding and spending transactions:
./bitcoind sendrawtransaction 010000000189632848f99722915727c5c75da8db2dbf194342a0429828f66ff88fab2af7d6000000008b483045022100abbc8a73fe2054480bda3f3281da2d0c51e2841391abd4c09f4f908a2034c18d02205bc9e4d68eafb918f3e9662338647a4419c0de1a650ab8983f1d216e2a31d8e30141046f55d7adeff6011c7eac294fe540c57830be80e9355c83869c9260a4b8bf4767a66bacbd70b804dc63d5beeb14180292ad7f3b083372b1d02d7a37dd97ff5c9effffffff0140420f000000000017a914f815b036d9bbbce5e9f2a00abd1bf3dc91e955108700000000

3c9018e8d5615c306d72397f8f5eef44308c98fb576a88e030c25456b4f3a7ac

./bitcoind sendrawtransaction 0100000001aca7f3b45654c230e0886a57fb988c3044ef5e8f7f39726d305c61d5e818903c00000000fd5d010048304502200187af928e9d155c4b1ac9c1c9118153239aba76774f775d7c1f9c3e106ff33c0221008822b0f658edec22274d0b6ae9de10ebf2da06b1bbdaaba4e50eb078f39e3d78014730440220795f0f4f5941a77ae032ecb9e33753788d7eb5cb0c78d805575d6b00a1d9bfed02203e1f4ad9332d1416ae01e27038e945bc9db59c732728a383a6f1ed2fb99da7a4014cc952410491bba2510912a5bd37da1fb5b1673010e43d2c6d812c514e91bfa9f2eb129e1c183329db55bd868e209aac2fbc02cb33d98fe74bf23f0c235d6126b1d8334f864104865c40293a680cb9c020e7b1e106d8c1916d3cef99aa431a56d253e69256dac09ef122b1a986818a7cb624532f062c1d1f8722084861c5c3291ccffef4ec687441048d2455d2403e08708fc1f556002f1b6cd83f992d085097f9974ab08a28838f07896fbab08f39495e15fa6fad6edbfb1e754e35fa1c7844c41f322a1863d4621353aeffffffff0140420f00000000001976a914ae56b4db13554d321c402db3961187aed1bbed5b88ac00000000

837dea37ddc8b1e3ce646f1a656e79bbd8cc7f558ac56a169626d649ebe2a3ba

# You can see these transactions at:
# http://blockchain.info/address/3QJmV3qfvL9SuYo34YihAf3sRCW3qSinyC
