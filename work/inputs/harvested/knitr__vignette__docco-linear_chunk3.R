# r2py crawler metadata
# package: knitr
# source_type: vignette
# topic: docco-linear_chunk3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\doc\docco-linear.Rmd
# lines: 4

suppressPackageStartupMessages(library(knitr))
n=300; set.seed(123)
par(mar=c(4,4,.1,.1))
plot(rnorm(n), rnorm(n), pch=21, cex=5*runif(n), col='white', bg='gray')