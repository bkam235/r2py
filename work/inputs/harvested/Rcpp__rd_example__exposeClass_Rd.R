# r2py crawler metadata
# package: Rcpp
# source_type: rd_example
# topic: exposeClass.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\Rcpp\help
# lines: 42

suppressPackageStartupMessages(library(Rcpp))
### Given the following C++ class, defined in file PopBD.h,
### the call to exposeClass() shown below will write a file
### src/PopBDModule.cpp containing a corresponding module definition.
###   class PopBD {
###     public:
###       PopBD(void);
###       PopBD(NumericVector initBirth, NumericVector initDeath);
###   
###       std::vector<double> birth;
###       std::vector<double> death;
###       std::vector<int> lineage;
###       std::vector<long> size;
###       void evolve(int);
###   
###   };
### A file R/PopBDClass.R will be written containing the one line:
###   PopBD <- setRcppClass("PopBD")
###
### The call below exposes the lineage and size fields, read-only,
### and the evolve() method.

exposeClass("PopBD",
      constructors =
        list("", c("NumericVector", "NumericVector")),
      fields = c("lineage", "size"),
      methods = "evolve",
      header = '#include "PopBD.h"',
      readOnly = c("lineage", "size"))

### Example with inheritance:  the class PopCount inherits from 
### the previous class, and adds a method table().  It has the same
### constructors as the previous class.
### To expose the table() method, and the inherited evolve() method and size field:

exposeClass("PopCount",
      constructors =
        list("", c("NumericVector", "NumericVector")),
      fields = c(size = "std::vector<long>"),
      methods = list("table", evolve = c("void", "int")),
      header = '#include "PopCount.h"',
      readOnly = "size")