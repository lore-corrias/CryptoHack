#!/usr/bin/env python

import requests
import hashlib
from tqdm import tqdm
from Crypto.Cipher import AES

URL = "https://aes.cryptohack.org"
WORDS = requests.get("https://gist.githubusercontent.com/wchargin/8927565/raw/d9783627c731268fb2935a731a618aa8e95cf465/words").text.splitlines()
CIPHERTEXT = requests.get(URL + "/passwords_as_keys/encrypt_flag/").json()["ciphertext"]
# print("[*] Ciphertext:", CIPHERTEXT)


for word in tqdm(WORDS):
    cipher = AES.new(hashlib.md5(word.encode()).digest(), AES.MODE_ECB)
    try:
        f = cipher.decrypt(bytes.fromhex(CIPHERTEXT))
        if f.startswith(b"crypto{"):
            print("[+] Key:", word)
            print("[!] Flag:", f.decode())
            break
    except ValueError as e:
        print(e)
        continue
