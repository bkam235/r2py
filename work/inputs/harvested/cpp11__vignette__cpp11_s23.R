# r2py crawler metadata
# package: cpp11
# source_type: vignette
# topic: cpp11_s23
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cpp11\doc\cpp11.R
# lines: 13

suppressPackageStartupMessages(library(cpp11))
gibbs_r <- function(N, thin) {
  mat <- matrix(nrow = N, ncol = 2)
  x <- y <- 0
  for (i in 1:N) {
    for (j in 1:thin) {
      x <- rgamma(1, 3, y * y + 4)
      y <- rnorm(1, 1 / (x + 1), 1 / sqrt(2 * (x + 1)))
    }
    mat[i, ] <- c(x, y)
  }
  mat
}