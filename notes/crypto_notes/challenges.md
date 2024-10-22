## Successive Powers
The following integers: $\{588,665,216,113,642,4,836,114,851,492,819,237\}$ are successive large powers of an integer $x$, modulo a three digit prime $p$.  
  
Find $p$ and $x$ to obtain the flag.

This means that we have a system of equations like:
$$
\begin{cases}
588 \equiv x^1 \mod p \\
665 \equiv x^2 \mod p \\
216 \equiv x^3 \mod p \\
... \\
237 \equiv x^{12} \mod p
\end{cases}
$$
We can restructure the system of equations like:
$$
\begin{cases}
588 &\equiv x \mod p \\
588x &\equiv 665 \mod p \\
665x &\equiv 216 \mod p \\
... \\
\end{cases}
$$
So getting the second one means finding a $x$:
$$
588^2 = 665 + kp \implies p = \frac{588^2-665}{k}
$$
$665 + k_2p= (558 + k_1p)^2$ 

$665 + p - 588^2 - 588p - p^2 = 0 \implies p^2 -587p + (588^2 - 665)$
