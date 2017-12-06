
## Iterative Techniques

vector norm 
:   a function from $\R^n$ to $\R$

:   $l_2$ norm is also called the Euclidean norm

:   $\rvert\rvert \mathbf{x} \rvert\rvert_2 = \left(\sum_{i=1}^nx_i^2\right)^{1/2}$

convergence
:   A sequence $\left\{\mathbf{x}^{(k)}\right\}_{k=1}^\infty$ of vectors in $\R^n$ is said to converge to $\mathbf{x}$ with respect to the norm $\rvert\rvert \cdot \rvert\rvert<\epsilon$, if given any $\epsilon>0$, there exists an integer $N(\epsilon)$ such that 

    $$\rvert\rvert\mathbf{x}^{(k)}-\mathbf{x}\rvert\rvert<\epsilon
      \text{, for all }k\geq N(\epsilon)$$

spectral radius
:   the spectral radius of a matrix $A$ is defined by 

    $$\rho(A)=\max\rvert\lambda\rvert|$$

    where $\lambda$ is an eigenvalue of $A$.

convergent matrices
:   an $n$ by $n$ matrix is convergent if for all $1\leq i,j \leq n$ 

    $$\lim_{k\to\infty}(A^k)_{ij}=0$$



```python

```
