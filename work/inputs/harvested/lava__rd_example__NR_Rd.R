# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: NR.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 13

suppressPackageStartupMessages(library(lava))
# Objective function with gradient and hessian as attributes
f <- function(z) {
   x <- z[1]; y <- z[2]
   val <- x^2 + x*y^2 + x + y
   structure(val, gradient=c(2*x+y^2+1, 2*y*x+1),
             hessian=rbind(c(2,2*y),c(2*y,2*x)))
}
NR(c(0,0),f)

# Parsing arguments to the function and
g <- function(x,y) (x*y+1)^2
NR(0, gradient=g, args=list(y=2), control=list(trace=1,tol=1e-20))