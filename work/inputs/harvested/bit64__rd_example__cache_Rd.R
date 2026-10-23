# r2py crawler metadata
# package: bit64
# source_type: rd_example
# topic: cache.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit64\help
# lines: 19

suppressPackageStartupMessages(library(bit64))
x <- as.integer64(sample(c(rep(NA, 9), 1:9), 32, TRUE))
  y <- x
  still.identical(x,y)
  y[1] <- NA
  still.identical(x,y)
  mycache <- newcache(x)
  ls(mycache)
  mycache
  rm(mycache)
  jamcache(x)
  cache(x)
  x[1] <- NA
  cache(x)
  getcache(x, "abc")
  setcache(x, "abc", 1)
  getcache(x, "abc")
  remcache(x)
  cache(x)