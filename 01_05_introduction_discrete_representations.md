
\newcommand{\vecu}{\mathbf{u}}

\newcommand{\ddx}{\frac{d}{dx}}

## Discrete Representations

At the core of this work is the analogy between discrete and continuous mathematics ---
matrix equations and differential equations. The time-independent Schrödinger equation ([@eq:time_independent_schrodinger]) 
is essentially the second-order differential equation 

$$H\psi=E\psi \implies -\frac{d^2 }{dx^2}\psi=\lambda \psi$$ {#eq:second_order_diff_eqn}

generally solved by $y=\cos \omega x$ and $y=\sin\omega x$ with $\lambda =\omega^2$. 


Analogously, we consider the matrix equation (and eigenproblem)

$$ - D\mathbf{u} = \lambda \mathbf{u}$$ {#eq:second_difference_eigenproblem}

where $D$ represents a difference matrix with a specific set of boundary conditions, 
$\mathbf{u}$ is an eigenvector, and $\lambda$ is an eigenvalue. 

### Representing a Vector in `numpy`

It helps to begin to think of this in terms of how we might represent a function in `numpy`.
Here, we represent the linear function, $f(x)=x$ as $\vecu$ as an evenly spaced vector 
from 0 to 1 with steps of $h=0.1$. 

```python
In [1]: import numpy

In [2]: u = numpy.linspace(0,1,11)

In [3]: u
Out[3]: array([ 0. ,  0.1,  0.2,  0.3,  0.4,  0.5,  0.6,  0.7,  0.8,  0.9,  1. ])
```

### Finite Differences

Consider the derivative:

$$f'(x)=\lim_{h\to 0} \frac{f(x+h)-f(x)}{h}$$ {#eq:first_derivative}

It is not possible to represent a function $f: \mathbb{R} \to \mathbb{R}$ computationally 
because computers are discrete in nature and require discrete representation. Nor is it
possible to symbolically represent an operation like taking the derivative. 
Toward a discrete representation, we consider our function as a vector and then look at the 
finite difference method, representing the derivative as a difference operator. 

Toward the difference operator we take

$$f'(x)\approx \frac{f(x+h)-f(x)}{h}$$ {#eq:first_difference}

Recalling that $\vecu[0]\approx f(0.0)$, 
$\vecu[1]\approx f(0.1)$, $\vecu[2]\approx f(0.2)$\dots,

\begin{align*}
\ddx\vecu[0] &= \frac{1}{0.1}\left(\vecu[1] -\vecu[0]\right) = 1\\
\ddx\vecu[1] &= \frac{1}{0.1}\left(\vecu[2] -\vecu[1]\right) = 1\\
\ddx\vecu[2] &= \frac{1}{0.1}\left(\vecu[3] -\vecu[2]\right) = 1\\
&\dots\\
\ddx\vecu[9] &= \frac{1}{0.01}\left(\vecu[10] -\vecu[9]\right) = 1\\
\ddx\vecu[10] &= \frac{1}{0.01}\left(\vecu[11] -\vecu[10]\right) = 1\\
\end{align*}

More generally, 

$$\frac{d}{dx}\mathbf{u}[x] \approx \frac{1}{h}\left(\mathbf{u}[x+h]-\mathbf{u}[x]\right)=
\frac{1}{h}\left(
\begin{matrix}
1 & -1 &  0 & \dots & 0 & 0 & 0 \\
0 & -1 & 1 & \dots &  0 & 0 & 0 \\
\vdots & \ & \ & \ddots & \ & \ & \vdots \\
0 & 0 & 0 & \dots & 1 & -1 & 0 \\
0 & 0 & 0 & \dots & 0 & 1 & -1 \\
\end{matrix}\right)\mathbf{u}=A \mathbf{u}
$$ {#eq:first_difference_equation}

Then the first derivative can be approximated by this matrix

$$\frac{d}{dx} \approx A = 
\frac{1}{h}\left(\begin{matrix}
1 & -1 &  0 & \dots & 0 & 0 & 0 \\
0 & -1 & 1 & \dots &  0 & 0 & 0 \\
\vdots & \ & \ & \ddots & \ & \ & \vdots \\
0 & 0 & 0 & \dots & 1 & -1 & 0 \\
0 & 0 & 0 & \dots & 0 & 1 & -1 \\
\end{matrix}\right)
$$ {#eq:first_difference_operator}

\pagebreak

###  Toward Second Difference Operator

Consider 

\begin{align*}
f''(x) &\approx \frac{f'(x+h)-f'(x-h)}{2h}\\
&\approx \frac{\frac{f(x+h)-f(x)}{2h}-\frac{f(x)-f(x-h)}{2h}}{2h}\\
&\approx \frac{f(x+h) - 2f(x) + f(x-h)}{h^2}\tag{with $2h$ recast as $h$}
\end{align*}

$$f''(x)\approx \frac{1}{h^2}\left(f(x+h) - 2f(x) + f(x-h)\right)$$  {#eq:second_difference}

Now consider the following discrete representation

```
          |  2 -1  0  0  0  0  0  0  0  0  0 | |0.00| = |-|
          | -1  2 -1  0  0  0  0  0  0  0  0 | |0.01| = |2| 
          |  0 -1  2 -1  0  0  0  0  0  0  0 | |0.04| = |2|
          |  0  0 -1  2 -1  0  0  0  0  0  0 | |0.09| = |2|
          |  0  0  0 -1  2 -1  0  0  0  0  0 | |0.16| = |2|
-1/(.01)  |  0  0  0  0 -1  2 -1  0  0  0  0 | |0.25| = |2|
          |  0  0  0  0  0 -1  2 -1  0  0  0 | |0.36| = |2|
          |  0  0  0  0  0  0 -1  2 -1  0  0 | |0.49| = |2|
          |  0  0  0  0  0  0  0 -1  2 -1  0 | |0.64| = |2|
          |  0  0  0  0  0  0  0  0 -1  2 -1 | |0.81| = |2|
          |  0  0  0  0  0  0  0  0  0 -1  2 | |1.00| = |-|
```

Note that the vector being multiplied by the matrix corresponds to the values of $f(x)=x^2$ at $x=0.0,0.1,0.2,\dots,0.8,0.9,1.0$. Note that the matrix is being multiplied by $\frac{1}{h^2}=\frac{1}{.01}$ where $h=0.1$ or the step of our vector representing $f(x)$. Note that the returned value is the constant 2 which corresponds to $f''(x)=2$.




```python

```
