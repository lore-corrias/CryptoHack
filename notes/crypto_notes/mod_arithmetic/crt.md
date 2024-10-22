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
there is an integer $a$ such that $x \equiv a \mod 935$. ## Challenges
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
c_1 \equiv (2 \cdot p + 3 \cdot q)^{e_1} \mod N \\
c_2 \equiv (5 \cdot p + 7 \cdot q)^{e_2} \mod N \\
}
$$

In order to solve this problem, start by elevating $c_1$ to $e_2$ and $c_2$ to $e_1$:
$$
{c_1}^{e_2} \equiv (a_1 \cdot p + b_1 \cdot q)^{e_1 \cdot e_2} \mod N
$$
By calculating the power of the binomial following the [Binomial Theorem](https://en.wikipedia.org/wiki/Binomial_theorem) we would get a polynomial like the following:
$$
(a_1 \cdot p)^{e_1e_2} +\ ...\ + (b_1 \cdot q)^{e_1e_2} \mod N 
$$
but we notice that the terms in the middle are all in the form $c\cdot p^i\cdot q^j$, where $c$ is any combination of $a$ and $b$, and $i$ and $j$ are $0 < i < e_1, 0 < j < e_2$. Since this terms all contain a product of some power of $p$ and $q$, calculating the modulo just cancels them out. So we have:
$$
c_1^{e_2} \equiv (a_1 \cdot p)^{e_1e_2} + (b_1 \cdot q)^{e_1e_2} \mod N
$$
Since we have $N = p \cdot q$, we can apply the [[crt]] in reverse (instead of going from a sistem of equations modulo $p, q$ to one equation modulo $N = p \cdot q$, we go the opposite way and split the equations) to get the following equations:
$$
\begin{cases}
c_1^{e_2} \equiv (a_1 \cdot p)^{e_1e_2} + (b_1 \cdot q)^{e_1e_2} \mod p \\
c_1^{e_2} \equiv (a_1 \cdot p)^{e_1e_2} + (b_1 \cdot q)^{e_1e_2} \mod q
\end{cases}
$$
the same can be done with $c_2^{e_1}$:
$$
\begin{cases}
c_2^{e_1} \equiv (a_2 \cdot p)^{e_1e_2} + (b_2 \cdot q)^{e_1e_2} \mod p \\
c_2^{e_1} \equiv (a_2 \cdot p)^{e_1e_2} + (b_2 \cdot q)^{e_1e_2} \mod q
\end{cases}
$$
In these cases, for the equations $\mod p$, the terms containing $p$ cancel out, and the same can be said for those $\mod q$. Applying this logic, we get these two equations:
$$
\begin{cases}
q_1 \equiv c_1^{e_2} \equiv (2p)^{e_1e_2} \mod q \\
q_2 \equiv c_2^{e_1} \equiv (5p)^{e_1e_2} \mod q
\end{cases}
$$
In order to factor $q$, we need a term $D$ that we know is divisible by both $q$ and $N$, so we can calculate $gcd(D,N)=q$. Such a term can be built as:
$$
D = 5^{e_1e_2}q_1 - 2^{e_1e_2}q_2
$$
We know that $D$ is divisible by $q$ because both $q_1$ and $q_2$ are. So we get:
$$
\displaylines{q = gcd(D,N) \\ p = \frac{N}{q}}
$$