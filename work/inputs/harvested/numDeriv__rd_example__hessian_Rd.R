# r2py crawler metadata
# package: numDeriv
# source_type: rd_example
# topic: hessian.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\numDeriv\help
# lines: 21

suppressPackageStartupMessages(library(numDeriv))
sc2.f <- function(x){
    n <- length(x)
    sum((1:n) * (exp(x) - x)) / n
    }

  sc2.g <- function(x){
    n <- length(x)
    (1:n) * (exp(x) - 1) / n
    }

  x0 <- rnorm(5)
  hess <- hessian(func=sc2.f, x=x0)
  hessc <- hessian(func=sc2.f, x=x0, "complex")
  all.equal(hess, hessc, tolerance = .Machine$double.eps)
  
#  Hessian = Jacobian of the gradient
  jac  <- jacobian(func=sc2.g, x=x0)
  jacc <- jacobian(func=sc2.g, x=x0, "complex")
  all.equal(hess, jac, tolerance = .Machine$double.eps)
  all.equal(hessc, jacc, tolerance = .Machine$double.eps)