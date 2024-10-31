# Notes about programming with math

## Conditions
Our goal is using indicators, i.e. functions that yield `0` when a condition doesn't apply and `1` where is does.  

### Negation
Negation is easy - assuming our input is also an indicator, we apply $1-f\left(x\right)$, which will turn a `0` into a `1` and vice-versa.

### Inequality
We can use the `arctan` function that turns a `0` into a `0` and all other inputs into non-zero values in the range $\left(-\frac{\pi}{2},\frac{\pi}{2}\right)$.  
We turn all negative values to positive ones by squaring, and then normalize by $\frac{\pi^2}{4}$ due to the squaring.  
This gives us a number between 0 and 1, where `0` is only yielded for the input `0`. Then, we simply use the ceiling function, which means all input turn into `1` except for the input `0`.  
Therefore, the condition `a != b` can turn into $1-\left\lceil\frac{4\arctan^2{\left(a-b\right)}}{\pi^2}\right\rceil$.
