Message server
==============

The server needs to implement the following two JSON-RPC calls:

- send(subject, body) => return some confirmation of the send
- receive() => return a list of new messages
