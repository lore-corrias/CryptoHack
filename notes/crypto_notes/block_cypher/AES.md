---
title: AES and Block Cyphers
---
- [[#Structure of AES|Structure of AES]]
	- [[#Structure of AES#`SubBytes`|`SubBytes`]]
	- [[#Structure of AES#`ShiftRows`|`ShiftRows`]]
	- [[#Structure of AES#`MixColumns`|`MixColumns`]]

Every block cipher performs so called "keyed permutations", meaning the the operations of text encryption map uniquely an *input block* to a single *output block*. This property is called *bijection* and it is fundamental to perform the process of decryption without errors.

> [!important] The term "block" just refers to a segment of the text or, more generally, any stream of a fixed number of bytes.

The key strength of a block cipher is that it leaves no hint on any aspect of the original plaintext, and in this way it makes the message basically indistinguishable from a random scrambling of random bits (in this regard, a cipher is considered *insecure* if there is a way for an attacker to retrieve the private key used for encryption in a way that's faster than just *bruteforcing it*).
The AES cipher uses a $128$ bit long encryption key, and trying to crack it by bruteforce is basically impossible. And for this reason, algorithms such as `AES-256` (using a $256$ bit long key) prove effective even against quantum-attacks (whereas public key ciphers like RSA don't, because of [Shor's Algorithm](https://en.wikipedia.org/wiki/Shor%27s_algorithm))

## Structure of AES
The basic strategy of the `AES` cipher to achieve a keyed permutation of the input is to perform a huge number of mixing operations on it, which are all dependent on the private key.

To start, we assume that we have a text to encrypt. The first step is to represent it as a $4 \times 4$ matrix of bytes

Second step expands the key in an operation that is called "key schedule": from the initial $128$ bit key, $11$ more keys each of length $128$ bit are derived, so that every distinct key can be applied to a different round.

The first key's bytes are `XOR`'d with the current plaintext. This step is crucial, because it provides a way to have a "keyed permutation" instead of a simple permutation.
		![](https://cryptohack.org/static/img/aes/AddRoundKey.png)

This first `XOR`'d text goes then through 10 different *rounds*, that perform these operations:
### `SubBytes`
Each byte of the *state* is substituted with another byte, according to a sort of "lookup table", called an **S-Box**.
![](https://cryptohack.org/static/img/aes/Substitution.png)
In order to understand why this step is necessary, we need to take a closer look at what it means for a cipher to be really *secure*. Famous mathematician and cryptographer *Claude Shannon* stated in 1945 that for an encryption scheme to be secure it has to add as much "**confusion**" in the encryption process as possible. This means that the harder it is to establish a relation between the plain and ciphertext, then the more secure the cipher is. Caesar's cipher, for example, is not secure, as the relation between the encrypted and plain text can be expressed as $ciphertext = plaintext + key$. Even algebraic relations, such as a polynomial in the form $ciphertext = x^4 + 51x^3 + x$ can be solved easily, and thus are not secure.

The purpose of the **S-Box** is exactly to hide even more the relation between the input and the output, so that the relation function that connects the two is **highly non-linear**. In this sense, the process of looking up a symbol in an S-Box is expressed by a function that takes the *modular inverse* in the Galois field $2^8$, and then applying the transformation. This can be expressed with the following polynomial:
$$
f(x) = 05x^{fe} + 09x^{fd} + f9x^{fb} + 25x^{f7} + f4x^{ef} + 09x^{df} + b5x^{bf} + 8fx^{7f} + 63
$$

This lookup function is calculated for each input value from $0x00$ to $0xff$.

### `ShiftRows`
The second step described by Shannon to obtain a valid cipher is called "diffusion". This can be simplified as a property stating that every single bit of the input should be spread to all the bits of the output.

After the substitution operated by the S-Box we have achieved confusion, but not diffusion, because the input bit can be reversed applying the same operation to the output bit (in this case, applying the inverse S-Box), and this undermines the cipher's security. To achieve a good level of algebraic complexity we need to alternate the substitutions with some scrambling operations (which can be reverted, however), so that each state is also influenced by the previous one. This desirable outcome in which one change in the input causes big changes in the output is called [Avalanche Effect](https://en.wikipedia.org/wiki/Avalanche_effect). This goal is achieved by the `ShiftRows` and `MixColumns` operations of a round.

The `ShiftRows` operation is the simplest, and it works like this:
1. The first row of the matrix is left untouched
2. The second row of the matrix is shifted one position to the left, wrapping it around
3. The third row of the matrix is shifted two positions to the left
4. The fourth row is shifted three positions to the left

In the end, the outcome is something like this:
![](https://cryptohack.org/static/img/aes/ShiftRows.png)
The goal of this simple operation is not to achieve real diffusion, but rather to make sure that each row is not encrypted independently from the others, a property that would degenerate AES into four, independent block ciphers.

### `MixColumns`

`MixColumns` is where the real diffusion happens, and that is why it is a bit complex. This operation perfoms *Matrix Multiplication in Rijandel's Galois field*, between the columns of the *state matrix* and a *preset matrix*, so that each byte of each column affects each byte of the resulting column. The details are complex, but the operation can be summarized in this picture:
![](https://cryptohack.org/static/img/aes/MixColumns.png)

As a last step, the operation `AddRoundKey` is repeated once again.

## Multiple Blocks
Up until now, we saw AES encryption with one single block of text. However, in normal circumstances it is necessary to encrypt chunks of data that occupy multiple blocks, and this is where **modes of operation** become necessary. These are a set of instructions on how to use the AES cipher for longer messages, and all of them introduce *serious weaknesses* when used incorrectly.

### Keys and Passwords
All keys of an AES cipher should be made of random bytes generated with a *Cryptographically-Secure pseudorandom number generator* (referred to as *CSPRNG*), because passwords and other kinds of predictable tokens are generally easy to break.

### ECB
ECB is the simplest mode of operation: each block is encrypted independently and appended to the output separately. This mode of operation is particularly vulnerable to "*oracles*". Consider this [ecb-oracle](https://aes.cryptohack.org/ecb_oracle/) challenge from CryptoHack:
```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


KEY = ?
FLAG = ?


@chal.route('/ecb_oracle/encrypt/<plaintext>/')
def encrypt(plaintext):
    plaintext = bytes.fromhex(plaintext)

    padded = pad(plaintext + FLAG.encode(), 16)
    cipher = AES.new(KEY, AES.MODE_ECB)
    try:
        encrypted = cipher.encrypt(padded)
    except ValueError as e:
        return {"error": str(e)}

    return {"ciphertext": encrypted.hex()}
```
We are given the possibility to encrypt an arbitrary text which will be appended before the `FLAG` to constitute the final plaintext. The whole result is then padded to ensure that it is exactly `16-byte` long.

The ECB mode of operation encodes the blocks as follows:
![](https://aes.cryptohack.org/static/img/aes/ECB_encryption.svg)

Notice how each block is encrypted separately, and since we have the possibility to append an arbitrary string to the flag before it is encrypted, our goal could be something like:
1. Find the length of the flag. This will be useful later, but in order to do so we can just append one character at a time until the ciphertext doubles in size (because of the padding). Once this happens, we know that $(n-1) + |flag| = 16$, where $n$ is the number of characters injected when $|ciphertext| = 32$,   and thus $|flag| = 16 - n + 1$.
2. We can now start bruteforcing the flag one character at a time. In order to do this, we start with the first one
	1. First step is to obtain a block of text that contains user input for $15$ bytes, so that the last one is left as being the first character of the flag. We can do this by asking our oracle to encode, for example, `\x10 * 15`. This way, our ciphertext will be in the form:
	   $$
	   | n \times 15 + flag[0] | + |flag[1:17] + | flag[17:31] | + ...
	   $$
	   where the $||$ represent the boundaries of a block, and $n \times 15$ is the string injected by the attacker. We'll refer to the first block as $b_0$, and we'll store it for now.
	2. Since we know that $b_0$ is the encryption of a text of which we know the first $15$ bytes, we can actually obtain the $16th$ (that is also the first character of the flag), by simply bruteforcing all of the $255$ possible combinations of $c$, the candidate for $flag[0]$, by asking the server to encrypt `\x10 * 15 + c` for each possible candidate. In every case, we need to compare the first block of our output to $b_0$, and once we'll eventually find a match we know that $c = flag[0]$
	3. Reiterate step 2 for $16$ times, but inject `\x10 * (15 - i)` in the first step ($i$ is the current step of the iteration), and `\x10 * (15 - i) + flag[:i] + c` in the second step. If you exhaust the space for one block (which means that the flag is longer than 16 bytes), than you can simply move to an extra block (and so you will add consider `15 * j - i`, where `j` is the current block number)
The script can be found in `block_ciphers/ecb_oracle.py`.


### CBC Encryption, ECB Decryption
The CBC mode of operation adds an extra layer of confusion to the encryption scheme. Before being encrypted, each plaintext block is `XOR`'d with the preceding block's ciphertext, while the first block is `XOR`'d with a so-called `IV`, or *initialization vector*, for short, which is usually made of $16$ random bytes. The final ciphertext is  $IV + ciphertext$
![](https://aes.cryptohack.org/static/img/aes/CBC_encryption.svg)
The decryption process requires instead to pass each block through the decryption steps, and then `XOR` the result with the preceding block's ciphertext, to get the relative block's plaintext. The first block's post-decryption part needs to be decoded with the initialization vector
![](https://www.researchgate.net/publication/362389340/figure/fig1/AS:11431281078760765@1660241201026/a-CBC-mode-encryption-b-CBC-mode-decryption.ppm)

Imagine now that we have a program like the following (this is taken from [ecbcbcwtf](https://aes.cryptohack.org/ecbcbcwtf/)):
```python
from Crypto.Cipher import AES


KEY = ?
FLAG = ?


@chal.route('/ecbcbcwtf/decrypt/<ciphertext>/')
def decrypt(ciphertext):
    ciphertext = bytes.fromhex(ciphertext)

    cipher = AES.new(KEY, AES.MODE_ECB)
    try:
        decrypted = cipher.decrypt(ciphertext)
    except ValueError as e:
        return {"error": str(e)}

    return {"plaintext": decrypted.hex()}


@chal.route('/ecbcbcwtf/encrypt_flag/')
def encrypt_flag():
    iv = os.urandom(16)

    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(FLAG.encode())
    ciphertext = iv.hex() + encrypted.hex()

    return {"ciphertext": ciphertext}
```
We can get the flag encrypted via `CBC`, but we are only able to decrypt it via `ECB`.

In order to understand how to decrypt the flag with a different mode of operation, let's try to represent the first `CBC` encrypted block. We could write it as:
$$
\text{block}_1 = enc_{cbc}(\text{plain}_1 \oplus IV)
$$
and since the `ECB` decryption acts on one single block, we would get:
$$
dec_{ecb}(\text{block}_1) = \text{plain}_1 \oplus IV
$$
But since we know $IV$, because $\text{ciphertext}_{cbc} = IV + \text{ciphertext}$, we can get the first plaintext block by performing:
$$
\text{plain}_1 = dec_{ecb}(\text{block}_1) \oplus IV
$$
More generally, the $n$th block of the CBC encrypted text can be written as:
$$
\text{block}_n = enc_{cbc}(\text{plain}_n \oplus \text{block}_{n-1}) \implies dec_{ecb}(\text{block}_n) = \text{plain}_n \oplus \text{block}_{n-1}
$$
Which means that retrieving the $n$th block of plaintext is as simple as:
$$
\text{plain}_n = dec_{ecb}(\text{block}_n) \oplus \text{block}_{n-1}
$$

