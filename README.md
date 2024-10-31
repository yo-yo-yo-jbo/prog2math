# Notes about programming with math

## Conditions
Our goal is using indicators, i.e. functions that yield `0` when a condition doesn't apply and `1` where is does.  

### Logical conditions
Negation (`logical not`) is easy - assuming our input is also an indicator, we apply $1-f\left(x\right)$, which will turn a `0` into a `1` and vice-versa.  
`Logical and` conditions are also easy, as we are working with indicators, we simply multiply conditions: `a and b` is really $ab$.  
`Logical or` is a bit more complicated, we could address it in several ways. One approach is adding all terms and test if the result is positive - we could implement that (see later about `non-negativity`), but at this point, since we have `and` and `not`, we could apply [The Morgan's laws](https://en.wikipedia.org/wiki/De_Morgan's_laws): `a or b` is equivalent to `not((not a) and (not b))`, which simply turns into this: `a or b` is $1-\left(1-a\right)\left(1-b\right)$.

### Inequality and equality
We can use the `arctan` function that turns a `0` into a `0` and all other inputs into non-zero values in the range $\left(-\frac{\pi}{2},\frac{\pi}{2}\right)$.  
We turn all negative values to positive ones by squaring, and then normalize by $\frac{\pi^2}{4}$ due to the squaring.  
This gives us a number between 0 and 1, where `0` is only yielded for the input `0`. Then, we simply use the ceiling function, which means all input turn into `1` except for the input `0`.  
Therefore, the condition `a != b` can turn into $\left\lceil\frac{4\arctan^2{\left(a-b\right)}}{\pi^2}\right\rceil$.  
Obviously we can now combine negation with inequality to test for equality: `a == b` is implemented as: $1-\left\lceil\frac{4\arctan^2{\left(a-b\right)}}{\pi^2}\right\rceil$.

### Non-negativity and bigger-than comparisons
To check if a number `x` is not negative, we could use the absolute value of it and see if it's equal to the original number.  
This can be implemented by calling the equality test on $\sqrt{x^2}$ and `x`: $1-\left\lceil\frac{4\arctan^2{\left(\sqrt{x^2}-x\right)}}{\pi^2}\right\rceil$.  
Given that capability, we can implement a `less-than-or-equal-to` test: to check if `a <= b`, we could check non-negativity on `b-a`: $1-\left\lceil\frac{4\arctan^2{\left(\sqrt{\left(b-a\right)^2}-\left(b-a\right)\right)}}{\pi^2}\right\rceil$.  
Obviously we could perform other things now too by running negations, e.g. `a < b` is equivalent to `not (b <= a)`.
