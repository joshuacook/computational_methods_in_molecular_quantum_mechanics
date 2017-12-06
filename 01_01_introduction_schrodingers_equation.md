
\mainmatter

# Introduction 

## Schrödinger's Equation
A dynamic quantum mechanical system
is governed by a linear partial differential equation
[@olver2014introduction;@strauss1992partial]. Developed by Erwin Schrödinger
and named for him, the equation is written

$$i\hbar\frac{\partial \psi}{\partial t}=H\psi$$ {#eq:time_dependent_schrodinger}

where $i=\sqrt{-1}$, $\hbar$ is Planck's constant, $H$ is the
self-adjoint\footnote{The adjoint of a linear operator $L$ is the unique
linear operator $L^*$ that satisfies $\llangle L[u],v\rrangle = \langle u,L^*v\rangle$
An operator is called self-adjoint if $L=L^*$. For a self-adjoint operator, the
eigenvalues are real and the eigenvectors for distinct eigenvalues are orthogonal.
Even where there is degeneracy in the eigenvalues, it is always possible for form
a complete basis set of orthogonal eigenvectors.},
linear operator known as the Hamiltonian, and $\psi$ is a wave function corresponding to
a quantum mechanical state of the system.

An eigenequation
is a relationship describing a vector or function that is invariant with respect to a
given linear operator. Given a linear operator $\Gamma: \mathbb{F}^n \to \mathbb{F}^n$,
$\lambda$ and $\psi$ are said to be an eigenvalue and eigenvector respectively of
$\Gamma$, if

$$\Gamma\psi=\lambda\psi \text{ for } \psi\neq0$$ {#eq:eigenequation}

Schrödinger's equation can be written independent of time as

$$H\psi=E\psi$$ {#eq:time_independent_schrodinger}

and takes the form of an eigenequation. Then, solutions are sets of eigenfunctions
representing quantum states, their corresponding eigenvalues representing energy levels.

In fact, these eigenfunctions are \emph{wave functions}, the most complete description that can be given of a physical system. Wave functions equate to the probability that a given measurement will result from a single measurement of an observable\footnote{It is part and parcel of the inherent strangeness of quantum mechanics that we can not describe a quantum system more accurately than by a measure of probability. More precisely, for a wavefunction $\phi(\mathbf{r})$, the probability that $\mathbf{r}$ is returned by a measurement is $p:=\rvert \phi(\mathbf{r})\rvert^2$.}.

Most treatments of quantum mechanics delineate a set of postulates
[@atkins2011molecular;@Eloranta:quantum;@singer2006linearity] necessary in the
formulation of quantum mechanics. For our purposes suffice it to assume that wave functions:

1. are functions
2. are continous and differentiable
3. are finite valued
4. are normal\footnote{Note that this fact combined with the self-adjointness of the
operators we are working with combine to give us \emph{orthonormal} wave functions.}

