---
title: AES and Block Cyphers
---
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