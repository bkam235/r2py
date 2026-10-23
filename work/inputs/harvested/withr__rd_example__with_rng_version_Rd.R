# r2py crawler metadata
# package: withr
# source_type: rd_example
# topic: with_rng_version.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\withr\help
# lines: 27

suppressPackageStartupMessages(library(withr))
RNGkind()
with_rng_version("3.0.0", RNGkind())
with_rng_version("1.6.0", RNGkind())

with_rng_version("3.0.0",
  with_seed(42, sample(1:100, 3)))

with_rng_version("1.6.0",
  with_seed(42, sample(1:100, 3)))

RNGkind()

fun1 <- function() {
  local_rng_version("3.0.0")
  with_seed(42, sample(1:100, 3))
}

fun2 <- function() {
  local_rng_version("1.6.0")
  with_seed(42, sample(1:100, 3))
}

RNGkind()
fun1()
fun2()
RNGkind()