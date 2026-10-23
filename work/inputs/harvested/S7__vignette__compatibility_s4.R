# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: compatibility_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\compatibility.R
# lines: 23

suppressPackageStartupMessages(library(S7))
rle <- function(x) {
  if (!is.vector(x) && !is.list(x)) {
    stop("'x' must be a vector of an atomic type")
  }
  n <- length(x)
  if (n == 0L) {
    new_rle(integer(), x)
  } else {
    y <- x[-1L] != x[-n]
    i <- c(which(y | is.na(y)), n)
    new_rle(diff(c(0L, i)), x[i])
  }
}
new_rle <- function(lengths, values) {
  structure(
    list(
      lengths = lengths,
      values = values
    ),
    class = "rle"
  )
}