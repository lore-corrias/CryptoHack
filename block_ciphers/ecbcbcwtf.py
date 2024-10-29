#!/usr/bin/env python

import requests
from Crypto.Util.strxor import strxor

CIPHERTEXT = bytes.fromhex(requests.get("https://aes.cryptohack.org/ecbcbcwtf/encrypt_flag/").json()["ciphertext"])
DECRYPT_URL = "https://aes.cryptohack.org/ecbcbcwtf/decrypt/%s"


blocks = [CIPHERTEXT[i:i+16] for i in range(0, len(CIPHERTEXT), 16)]
plaintext = b""

for i in range(1, len(blocks)):
    nth_block_decrypted = bytes.fromhex(requests.get(DECRYPT_URL % blocks[i].hex()).json()["plaintext"])
    plaintext += strxor(nth_block_decrypted, blocks[i-1])

print(plaintext)
