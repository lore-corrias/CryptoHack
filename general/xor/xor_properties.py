#!/usr/bin/env python3


"""
Below is a series of outputs where three random keys have been XOR'd together and with the flag. Use the above properties to undo the encryption in the final line to obtain the flag.
"""


def xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])


KEY1 = bytes.fromhex("a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313")
# KEY2 ^ KEY1 = "37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e"
# KEY2 ^ KEY3 = "c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1"
# FLAG ^ KEY1 ^ KEY3 ^ KEY2 = "04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf"

KEY2 = xor(KEY1, bytes.fromhex("37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e"))
KEY3 = xor(KEY2, bytes.fromhex("c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1"))

"""
since we have 

key2 = key1 ^ 2nd = 1st ^ 2nd
key3 = key2 ^ 3rd = 1st ^ 2nd ^ 3rd

then

flag = 4th ^ key2 ^ key3 ^ key1
flag = 4th ^ 1st ^ 2nd ^ 1st ^ 2nd ^ 3rd ^ 1st
flag = 1st ^ 3rd ^ 4rd
"""

flag = xor(
    xor(
        KEY1,
        bytes.fromhex("c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1"),
    ),
    bytes.fromhex("04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf"),
)

print("[*] Flag:", flag)
