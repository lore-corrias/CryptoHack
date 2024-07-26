#!/usr/bin/env python3

from pwn import *
import json


"""
For this challenge, connect to socket.cryptohack.org on port 11112.
Send a JSON object with the key buy and value flag.
"""

with remote("socket.cryptohack.org", 11112) as sock:
    sock.send(json.dumps({"buy": "flag"}))
    flag = sock.recvall()


print("[*] Flag:", flag)
