#!/usr/bin/python

import numpy, numpy.linalg, scipy.linalg, scipy.sparse

def secondDiff(type,n=10,sparse=False):
  '''
  secondDiff Create finite difference model matrix.
  TYPE is one of the characters 'D', 'R', 'N', or 'C'.
  3rd argument is boolean for sparseness
  '''
  e = numpy.ones(n)
  e_off = numpy.ones(n-1)
  D = scipy.sparse.csr_matrix(
    scipy.sparse.diags([e_off,-2*e,e_off],[-1,0,1]))

  if (str(type) == 'R' or str(type) == 'T' or 
    str(type) == 'N' or str(type) == 'B'):
    D[0,0] = -1
  if (str(type) == 'N' or str(type) == 'B'): 
    D[n-1,n-1] = -1
  if str(type) == 'C':
    D[0,n-1] = 1
    D[n-1,0] = 1

  if sparse == False: return D.todense()
  else: return D
  
def K_theta(k,n):
  return k*numpy.pi/(n+1)

def K_eigenvalues(n):
  return 2*numpy.ones(n) - 2*numpy.cos(K_theta(numpy.linspace(n,1,n),n))

def K_eigenfunction(k,n):
  vec = numpy.sin(K_theta(numpy.linspace(1,n,n),n)*k)
  return vec/numpy.linalg.norm(vec)
  
def my_eig(n):
  vals = []
  vals.append(K_eigenvalues(n))
  eigenvectors = numpy.matrix(K_eigenfunction(1,n))
  for i in range(n-1):
    eigenvectors = numpy.r_[eigenvectors,numpy.matrix(K_eigenfunction(i+2,n))]
  vals.append(eigenvectors)
  return vals
  
if __name__ == "__main__":

  import time
  
  bang = int(time.time())
  output_file = "output_" + str(bang) + ".csv"
  f = open(output_file, 'w')
  
  for i in range(3,5000):
    matrix = secondDiff('D',i)
    clocked_my = 100000
    for _ in range(3):
      bang_my = time.time()
      my_eig(i) 
      clocked_my = min(clocked_my, (time.time() - bang_my))
    clocked_sys = 100000
    for _ in range(3):
      bang_sys = time.time()
      numpy.linalg.eig(matrix)
      clocked_sys = min(clocked_sys, (time.time() - bang_sys))
    results = [i, clocked_my, clocked_sys] # , result_sys.best
    f.write(str(results)+"\n")
    
    
    