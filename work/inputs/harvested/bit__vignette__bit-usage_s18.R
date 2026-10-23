# r2py crawler metadata
# package: bit
# source_type: vignette
# topic: bit-usage_s18
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\doc\bit-usage.R
# lines: 13

suppressPackageStartupMessages(library(bit))
r <- ri(1, 2^16, 2^20) # sample(2^20, replace=TRUE, prob=c(.125, 875))
all.as <- list(
  double = as.double,
  integer= as.integer,
  logical = as.logical,
  bit = as.bit,
  bitwhich = as.bitwhich,
  which = as.which,
  ri = function(x) x
)
all.types <- lapply(all.as, function(f) f(r))
sapply(all.types, object.size)