#!/usr/bin/env python3


"""
Given the string label, XOR each character with the integer 13.
Convert these integers back to a string and submit the flag as crypto{new_string}.
"""


def xor(a, b):
    return [ord(x) ^ b for x in a]


message = "label"


flag = "".join(chr(x) for x in xor(message, 13))

print("[*] Flag:", flag)
