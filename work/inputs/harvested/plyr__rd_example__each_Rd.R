# r2py crawler metadata
# package: plyr
# source_type: rd_example
# topic: each.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\plyr\help
# lines: 13

suppressPackageStartupMessages(library(plyr))
# Call min() and max() on the vector 1:10
each(min, max)(1:10)
# This syntax looks a little different.  It is shorthand for the
# the following:
f<- each(min, max)
f(1:10)
# Three equivalent ways to call min() and max() on the vector 1:10
each("min", "max")(1:10)
each(c("min", "max"))(1:10)
each(c(min, max))(1:10)
# Call length(), min() and max() on a random normal vector
each(length, mean, var)(rnorm(100))