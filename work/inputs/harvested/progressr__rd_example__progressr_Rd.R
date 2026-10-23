# r2py crawler metadata
# package: progressr
# source_type: rd_example
# topic: progressr.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\progressr\help
# lines: 12

library(progressr)

xs <- 1:5

with_progress({
  p <- progressor(along = xs)
  y <- lapply(xs, function(x) {
    Sys.sleep(0.1)
    p(sprintf("x=%g", x))
    sqrt(x)
  })
})