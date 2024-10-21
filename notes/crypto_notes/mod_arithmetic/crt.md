---
title: Chinese Remainder Theorem
tags:
  - modular
  - arithmetic
---
# CRT - Chinese Remainder Theorem
The CRT can be applied to solve a theorem of linear congruences **if** their modules are coprime ($\forall n^i, n^j \in \{n^1, n^2, ..., n^i\}, n^i \neq n^j\ |\ gcd(n^i,n^j)=1$). If:
$$
\displaylines{x \equiv a^1 \mod n^1 \\
x \equiv a^2 \mod n^2 \\
... \\
x \equiv a^n \mod n^n}
$$
there is one solution $x \equiv a \mod N$, where N = $n^1 \cdot n^2 \cdot\ ...\ \cdot n^n$. For example:
$$
\displaylines{x \equiv 2 \mod 5 \\x \equiv 3 \mod 1 \\x \equiv 5 \mod 17 \\}
$$
there is an integer $a$ such that $x \equiv a \mod 935$.
## Challenges
### adriens-signs
A custom encryption algorithm that uses modular arithmetic. The encryption is:
1. the message is encoded in binary
2. consider $a=288260533169915, p=1007621497415251$
3. for each byte $b$:
	1. generate a random integer $e, 1 < e < p$.
	2. calculate $n \equiv a^e \mod p$
		1. if $b == 1$, then $n$ is added to the cyphertext
		2. else, $-n \mod p$ is added to the cyphertext

notice that $p$ is of the form $p \equiv 3 \mod 4$.  If we did not have the case of the bit $0$, we would have that each bit of the flag would be in the form:
$$
n = a^e \mod p
$$
and if we calculated $x \equiv n^{(\frac{p-1}{2})} \mod p$, we'd have that $x \in \{1, -1\}$ (this is [[legendre-symbol]], and $n$ is never equal to $0$). But how can we use this?
We can also see that the Legendre symbol for $(\frac{a}{p}) = 1$, meaning that also $(\frac{a^e}{p}) = 1$, for any value of $e$. This is our first case, meaning we can tell if the byte encrypted was a $1$ by calculating its Legendre's symbol. Can we also tell the case where $b=1$?
This is equivalent to calculating the value of the following expression:
$$
x = (\frac{-(a^e)}{p}) = (\frac{-1}{p}) = (-1)^{\frac{(p-1)}{2}} \mod p \equiv -1
$$
This is because $\frac{(p-1)}{2}$ is odd ($p \equiv 3 \mod 4$). Since the value of $-n \mod p$ is always $-1$, we know how to differentiate between the two cases
### Modular Binomials
Arrange the following equations to get $p, q$:
$$
\displaylines{
N = p \cdot q \\
c_1 = (2 \cdot p + 3 \cdot q)^{e_1} \mod N \\
c_2 = (5 \cdot p + 7 \cdot q)^{e_2} \mod N \\
}
$$

