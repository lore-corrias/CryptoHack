#!/usr/bin/env python

import requests
import time
import string


URL = "https://aes.cryptohack.org/ecb_oracle/encrypt/%s"

current_block = 1
flag = "crypto{p3n6u1n5_h473_3cb}" # set to empty if you want to bruteforce the flag

while len(flag) == 0 or flag[-1] != "}":
    # the (+1) is needed because we cannot ask to encrypt empty messages
    current_block = (len(flag) + 1) // 16 + 1
    # Generating string to inject
    block_to_encrypt = (b"A" * (16 * current_block - len(flag) - 1)).hex()
    # Retrieving the encrypted block to be bruteforced
    # print(URL % block_to_encrypt)
    b0 = bytes.fromhex(requests.get(URL % block_to_encrypt).json()["ciphertext"])[(16 * (current_block - 1)):(16 * current_block)]

    # Bruteforcing the last character of the block
    for c in string.printable:
        block_candidate = (b"A" * (16 * current_block - len(flag) - 1) + flag.encode() + c.encode()).hex()
        candidate_b0 = bytes.fromhex(requests.get(URL % block_candidate).json()["ciphertext"])[16 * (current_block - 1):(16 * current_block)]
        print("[*] Trying", c, end="\r")
        if b0 == candidate_b0:
            flag += c
            print("[+] Found character:", flag)
            break
        time.sleep(0.2)
    else:
        print("[-] Failed to find a character")
        exit()
