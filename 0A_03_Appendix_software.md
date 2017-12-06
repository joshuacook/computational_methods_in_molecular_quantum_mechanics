
## C


\paragraph{GSL}
Central to this work is the [GNU Scientific Library](http://www.gnu.org/software/gsl/) which offers implementations of `openblas` (Open Basic Linear Algebra System) and `lapack` (Linear Algebra Package) necessary for the completion of this work. We have used `homebrew` to install `gsl` and `pkg-config` 

```
$ brew install pkg-config
$ brew install gsl
$ pkg-config --libs gsl
-L/usr/local/Cellar/gsl/1.16/lib -lgsl -lgslcblas -lm
```

and then added the linker statements to our makefile:

```
#Tool Definitions
CC=gcc
CFLAGS=-I. -I$(PATHU) -DTEST
CFLAGS+=-I/usr/local/opt/openblas/include
CFLAGS+=-lgsl -lgslcblas -lm
```

\paragraph{Known Eigenvalues}
We have written a short python script in order to calculate a few known eigenvalues, in this case for the 4th order Hibert Matrix.

```
import numpy
import scipy
from scipy.linalg import *

h4 = hilbert(4)
eigs_h4 = eig(h4)
print eigs_h4
```

\paragraph{Test-Driven Development}
We begin the project with a simple tests to verify the known eigenvalues we have previously generated. 

```
#include <stdio.h>
#include <math.h>
#include <gsl/gsl_math.h>
#include <gsl/gsl_eigen.h>
#include "minunit.h"

#define DIMENSION_OF(a) (sizeof(a)/sizeof(a[0]))

gsl_vector * symmetric_eigenvalues(double * data, int return_values);

float round_to_5_places(float num);

int tests_run = 0;

double expected_eigenvalues[] = {1.500214,0.169141,0.006738,0.000097};

double fourth_order_hilbert[] =
{
  1.0  , 1/2.0, 1/3.0, 1/4.0,
  1/2.0, 1/3.0, 1/4.0, 1/5.0,
  1/3.0, 1/4.0, 1/5.0, 1/6.0,
  1/4.0, 1/5.0, 1/6.0, 1/7.0
};

static char * test_find_eigenvalues()
{
  gsl_vector * actual_eigenvalues = symmetric_eigenvalues(fourth_order_hilbert,0);

  for (int i = 0; i < DIMENSION_OF(expected_eigenvalues); i++)
  {
     float expected = expected_eigenvalues[i];
     float actual = round_to_5_places(gsl_vector_get(actual_eigenvalues, i));

     printf("\nexpected: %f actual: %f\n",
       expected,actual);
     mu_assert("error, eigenvalues do not match",
         expected == actual);
  }
  return 0;
}

static char * all_tests()
{
  mu_run_test(test_find_eigenvalues);
  return 0;
}

int main(int argc, char **argv)
{
  char * result = all_tests();
  if (result != 0)
  {
    printf("%s\n", result);
  }
  else
  {
    printf("All Tests Passed\n");
  }
  printf("Tests run: %d\n", tests_run);

  return result != 0;
}

gsl_vector * symmetric_eigenvalues(double * data, int return_values)
{
  gsl_matrix_view my_matrix = gsl_matrix_view_array (data, 4, 4);

  gsl_vector * my_evals = gsl_vector_alloc (4);
  gsl_matrix * my_evecs = gsl_matrix_alloc (4, 4);

  gsl_eigen_symmv_workspace * my_workspace = gsl_eigen_symmv_alloc (4);

  gsl_eigen_symmv (&my_matrix.matrix, my_evals, my_evecs, my_workspace);

  gsl_eigen_symmv_free (my_workspace);

  gsl_eigen_symmv_sort (my_evals, my_evecs, GSL_EIGEN_SORT_ABS_DESC);

  return my_evals;
}

float round_to_5_places(float num)
{
  float nearest = roundf(num * 1000000) / 1000000;
  return nearest;
}
```

\paragraph{Comments and Further Consideration}
I am not pleased with this particular test of the Symmetic Eigensolver implemented in GSL. It is very "numerical". I think a better test would be more mathematical, such as a test of any matrix and the eigenequation itself, $Ax=\lambda x$. I did, however, confirm that MinUnit is an excellent way to begin to implement a TDD mindset in C development. I think that the next step is to begin to write more tests around the openBlas implementation in the GSL.



\paragraph{MinUnit}
As per MinUnit's description, "MinUnit is an extremely simple unit testing framework written in C. It uses no memory allocation, so it should work fine under almost any circumstance, including ROMable code."

```
/* file: minunit.h */
 #define mu_assert(message, test) do { if (!(test)) return message; } while (0)
 #define mu_run_test(test) do { char *message = test(); tests_run++; \
                                if (message) return message; } while (0)
 extern int tests_run;
```

As per MinUnit's description: "No, that's not a typo. It's just 3 lines of code."

MinUnit has also been added to `tools`.

I wanted to be able to add more information to tests being run using the [`minunit.h`](http://www.jera.com/techinfo/jtns/jtn002.html) testing harness. In particular, I wanted to think of a test run as a "test" and an individual assert within that test run as a subtest. I wanted to be able to name each of these and have their status displayed in `STDOUT`. 

\paragraph{My MinUnit Implementation}
```
/* file: my_minunit.h */
#define mu_assert(subtest_desc, test,message) do { \
   if (!(test)) { \
   printf("subtest: \"%s\" FAILED\n", subtest_desc); \
   return message; \
   } \
   else { \
     printf("subtest: \"%s\" PASSED\n", subtest_desc); \
   } \
} while (0)

#define mu_run_test(test_desc,test) do { \
  printf("\nTest: \"%s\"\n",test_desc); \
  char *message = test(); tests_run++; \
  if (message) return message; } while (0)

extern int tests_run;
```

A little less minimal but still small. I also added this file to `/usr/include` so as to not have to tell `gcc` where to find it.

\paragraph{A typical output}
```

Test: "Test of GSL"
y: -0.177597     expected_y: -0.177597
subtest: "value of zero order Bessel function of the first kind" PASSED

Test: "Test of Rectangular Complex Number Struct"
subtest: "real part of a rectangular complex number" PASSED
subtest: "imaginary part of a rectangular complex number" PASSED
subtest: "real part of a rectangular complex number after redefinition" PASSED
subtest: "imaginary part of a rectangular complex number after redefinition" PASSED

All Tests Passed
Tests run: 2
```

\paragraph{Spec file for this output}

```
#include <stdio.h>
#include <gsl/gsl_sf_bessel.h>
#include <gsl/gsl_complex_math.h>
#include <math.h>
#include <my_minunit.h>

int tests_run = 0;
float round_to_6_places(float num);

static 
char * test_gsl_via_0_order_bessel_function_of_the_first_kind ()
{
  double x = 5.0;
  double y = round_to_6_places(gsl_sf_bessel_J0 (x));
  double expected_y = round_to_6_places(-1.775967713143382920e-01);
  printf("y: %f \t expected_y: %f\n",y,expected_y);
  mu_assert
  (
    "value of zero order Bessel function of the first kind",
    y == expected_y,
    "y: not equal to expected_y" 
  );
  return 0;
}

static
char * test_gsl_rectangular_complex_number_struct()
{
  double x = 2.43728;
  double y = 3.23412;

  gsl_complex test_rect_complex_number = gsl_complex_rect ( x, y ); 

  mu_assert
  (
    "real part of a rectangular complex number",
    GSL_REAL(test_rect_complex_number) == x,
    "real part of rectangular complex number does not match expected" 
  );

  mu_assert
  (
    "imaginary part of a rectangular complex number",
    GSL_IMAG(test_rect_complex_number) == y,
    "imaginary part of rectangular complex number does not match expected" 
  );

  GSL_SET_REAL(&test_rect_complex_number,y);
  GSL_SET_IMAG(&test_rect_complex_number,x);
  
  mu_assert
  (
    "real part of a rectangular complex number after redefinition",
    GSL_REAL(test_rect_complex_number) == y,
    "redefined real part of rectangular complex number does not match expected" 
  );

  mu_assert
  (
    "imaginary part of a rectangular complex number after redefinition",
    GSL_IMAG(test_rect_complex_number) == x,
    "redefined imaginary part of rectangular complex number does not match expected" 
  );

  return 0;
}  

static 
char * all_tests ()
{
  mu_run_test("Test of GSL", test_gsl_via_0_order_bessel_function_of_the_first_kind); 
  mu_run_test("Test of Rectangular Complex Number Struct", 
              test_gsl_rectangular_complex_number_struct);
  return 0;
}

int 
main(int argc, char **argv)
{
  char * result = all_tests();
  if (result != 0)
  {
    printf("%s\n", result);
  }
  else
  {
    printf("\nAll Tests Passed\n");
  }
  printf("Tests run: %d\n", tests_run);

  return result != 0;
}

float 
round_to_6_places(float num)
{
  float nearest = roundf(num * 10000000) / 10000000;
  return nearest;
}
```



## Python

While Python comes preinstalled with Mac OS X, installing through homebrew ensures that you have the most updated version as well as moves the management of Python to homebrew. 

```
brew install python 
```

Python comes installed by default, but best to get the latest and greatest. 

The above installs `pip`.

\paragraph{Install Basic Python Packages}

Most of the pip installs require that they be run as `sudo`. `brew` is not a fan of `sudo` and should not have the same requirements. 

```
pip install numpy
pip install scipy
pip install matplotlib
```

\paragraph{Python as a Tool for Developing C Algorithms}

emulating minunit in python [[Needs Work]]

\paragraph{IPython}

```
pip install ipython
```

This did not install all of the dependencies required to run IPython notebook. It was fairly straightforward to identify the missing dependencies, however, by attempting to run `IPython Notebook`.

```
ipython notebook 
```

The following three dependencies were succesively required:

```
pip install pyzmqi
pip install jinjaz
pip install tornado
```

\paragraph{Numpy}



\paragraph{Scipy}

\paragraph{Fabric}

## Unix-Like

\paragraph{Pandoc}
If you need to convert files from one markup format into another, pandoc is your swiss-army knife. [Pandoc](http://johnmacfarlane.net/pandoc/) can convert documents in markdown, reStructuredText, textile, HTML, DocBook, LaTeX, MediaWiki markup, TWiki markup, OPML, Emacs Org-Mode, Txt2Tags, Microsoft Word docx, EPUB, or Haddock markup to

- HTML formats: XHTML, HTML5, and HTML slide shows using Slidy, reveal.js, Slideous, S5, or DZSlides.
- Word processor formats: Microsoft Word docx, OpenOffice/LibreOffice ODT, OpenDocument XML
- Ebooks: EPUB version 2 or 3, FictionBook2
- Documentation formats: DocBook, GNU TexInfo, Groff man pages, Haddock markup
- Page layout formats: InDesign ICML
- Outline formats: OPML
- TeX formats: LaTeX, ConTeXt, LaTeX Beamer slides
- PDF via LaTeX
- Lightweight markup formats: Markdown, reStructuredText, AsciiDoc, MediaWiki markup, DokuWiki markup, Emacs Org-Mode, Textile
- Custom formats: custom writers can be written in lua.

Pandoc was (and is) used to render "final" pdfs of the work done. Pandoc files were written in a hybrid of markdown (for document formatting) and Latex (for math rendering) that mirror the presentation format of IPython Notebooks.

\paragraph{Install Pandoc}

```
brew install pandoc
```

You will need a reasonably robust \LaTeX installation.




```python

```
