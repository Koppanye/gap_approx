# Approximating the integrality gap of certain formulations up to some error

We will investigate the special case of the restricted assignment 
with 2 values, but the method potentially works for other problems as well.

The goal is the following: instead of considering the real integrality gap 
(currently known to be at most 5/3), we implement the idea of 
core instances. Given an error tolerance epsilon, we discretize the set
of all potential inputs with the epsilon-grid. 

On this finite set, we calculate the gap g (for small dimensions, say
n = 10, m = 4), and by this we are able to derive an upper bound of 
g + (n x epsilon) for the "real gap" in this small dimensions.

For a small enough epsilon, we hope to gain further insight 
on the "real gap" (so far known to be between 3/2 and 5/3) by examining
the experimental bound. If gap + (n x epsilon) is smaller, we could
state a conjecture that the "real gap" is that specific value 
(provided that we are able to determine it), and try coming up with
better approximation algorithms. On the other hand, if the
"empirical gap" seems close to 5/3, the conjecture could be that
the real gap is 5/3 as well, and researchers could channel efforts 
to find instances with this specific gap.

# TLDR:

Emprically approximating the gap could point us in the direction of 
either design better approximating algorithms, or constructing instances
with higher integrality gaps than the current champion (3/2).
