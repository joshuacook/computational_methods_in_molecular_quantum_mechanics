


# Power Method

## Solving Molecular Quantum Mechanics Problems Computationally

At its essence the work in Dr. Eloranta's lab is an extension of the simple power method for finding an eigenvector. 
Also known as the Von Mises Iteration, the simple power method operates on a few well conditionings, all of which 
are satisfied by our Hamiltonian matrices --- namely we require self-adjoint matrices, and all that this implies. 

The power method will only return the dominant eigenvector of an operator. Essentially, the next vector in the iteration
is calculated by multiplying the current vector by the matrix being examined and then normalizing.

\vfill

\pagebreak


## Simple Power Method

1. Choose a starting vector $\mathbf{x}^{(0)}\in\mathbb{R}^n$ with
$\rvert\rvert\mathbf{x}^{(0)}\rvert\rvert=1$.
2. $k=0$
3. `while` some convergence criteria is not satisfied

    i. $k:=k+1$
    ii. $\mathbf{y}^{(k)}:=A\mathbf{x}^{(k-1)}$
    iii. $\mu_k:=\rvert\rvert\mathbf{y}^{(k)}\rvert\rvert$
    iv. $\mathbf{x}^{(k)}:=\mathbf{y}^{(k)}/\mu_k$

The eigenvalue can be found by calculating

\begin{align*}
\lambda u &= A u\\
u^T\lambda u &= u^TA u\\
\lambda &= u^TAu \tag{because $u$ is normalized}
\end{align*}

\vfill

\pagebreak

Here we define an iteration and that iterate 100 times to find our the eigenvector associated with the largest eigenvalue.

```
def power_iteration(A,u,n):
  for i in range(n):
    u      = A.dot(u)
    mu     = numpy.sqrt(u.dot(u))
    u      = u/mu
  eigvec = u
  eigval = eigval = u.dot(A.dot(u))
  return eigval, eigvec

In [1]: import numpy, scipy.linalg, numpy.random

In [2]: B = numpy.random.rand(4,4)

In [3]: C = B.dot(B.T) # returns a symmetric matrix

In [4]: y = numpy.random.rand(4)

In [5]: power_iteration(C,u,100)
Out[5]: (5.4509787314661642,
 array([ 0.57243721,  0.54380344,  0.38428034,  0.47845802]))

In [6]: scipy.linalg.eigh(C,eigvals=(3,3))
Out[6]:
(array([ 5.45097873]), 
 array([[-0.57243721],
        [-0.54380344],
        [-0.38428034],
        [-0.47845802]]))
```


### Comparison of Timing

```
In [7]: %timeit power_iteration(C,u,100)
1000 loops, best of 3: 351 µs per loop

In [8]: %timeit scipy.linalg.eigh(C,eigvals=(3,3))
The slowest run took 6.32 times longer than the fastest. 
This could mean that an intermediate result is being cached
10000 loops, best of 3: 26 µs per loop
```

It is shown that our power iteration is considerably slower than the built-in eigensolver. We are, however, hard coding the number of iterations required. 


### Stopping Criteria

It would behoove us to explore a better stopping criteria than simply iterate 100 times. Toward this we propose the use of the norm of the residual vector

$$\mathbf{r}=A\vecu^*-\lambda^*\vecu^*$$ 

We can then stop our calculation when $\rvert\rvert\mathbf r \rvert\rvert<\epsilon$ for any desired $\epsilon$.

```
def power_iteration(A,u,n,eps=0.00001):
  r_mag = 1
  while(r_mag > eps):
    u      = A.dot(u)
    mu     = numpy.sqrt(u.dot(u))
    u      = u/mu
    eigval = eigval = u.dot(A.dot(u))
    r      = A.dot(u)-eigval*u
    r_mag  = numpy.sqrt(r.dot(r))
  eigvec = u
  return eigval, eigvec

In [9]: %timeit power_iteration(C,u,100)
The slowest run took 6.79 times longer than the fastest. 
This could mean that an intermediate result is being cached
10000 loops, best of 3: 42.9 µs per loop
```

While we are not beating the built-in solver, we are certainly within an order of magnitude and are satisfied with these results. 

