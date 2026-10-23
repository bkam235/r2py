# r2py crawler metadata
# package: lava
# source_type: vignette
# topic: influencefunction_s34
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\doc\influencefunction.R
# lines: 11

suppressPackageStartupMessages(library(lava))
set.seed(1)
y <- cbind(rnorm(1e5))
N <- 2e2 ## Number of aggregated groups, the number of observations in the new IF
id <- foldr(nrow(y), N, list=FALSE)
Print(cbind(table(id)))

## Aggregated IF
e <- estimate(cbind(y), id = id) 
object.size(e)
e