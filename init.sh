#!/bin/bash

bitcoincmd="bitcoind"

exec 6>&1 7>&2 1>/dev/null 2>/dev/null
if ! $bitcoincmd getinfo; then
    echo starting server 1>&6
    # Prepare a clean exit
    clean () { $bitcoincmd stop; }
    trap clean EXIT

    # Run server and wait for it to respond
    $bitcoincmd
    while :; do
        $bitcoincmd getinfo && break
    done

    # Wait for the node to update
    while :; do
        lastblk="$(curl http://blockexplorer.com/testnet/q/getblockcount 2>/dev/null)"
        curblk="$($bitcoincmd getblockcount)"
        echo "$curblk out of $lastblk" 1>&6
        [ "$lastblk" = "$curblk" ] && break
        sleep 5
    done
fi
exec 1>&6 2>&7
