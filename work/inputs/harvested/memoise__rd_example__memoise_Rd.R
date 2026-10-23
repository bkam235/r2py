# r2py crawler metadata
# package: memoise
# source_type: rd_example
# topic: memoise.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\memoise\help
# lines: 55

suppressPackageStartupMessages(library(memoise))
# a() is evaluated anew each time. memA() is only re-evaluated
# when you call it with a new set of parameters.
a <- function(n) { runif(n) }
memA <- memoise(a)
replicate(5, a(2))
replicate(5, memA(2))

# Caching is done based on parameters' value, so same-name-but-
# changed-value correctly produces two different outcomes...
N <- 4; memA(N)
N <- 5; memA(N)
# ... and same-value-but-different-name correctly produces
#     the same cached outcome.
N <- 4; memA(N)
N2 <- 4; memA(N2)

# memoise() knows about default parameters.
b <- function(n, dummy="a") { runif(n) }
memB <- memoise(b)
memB(2)
memB(2, dummy="a")
# This works, because the interface of the memoised function is the same as
# that of the original function.
formals(b)
formals(memB)
# However, it doesn't know about parameter relevance.
# Different call means different caching, no matter
# that the outcome is the same.
memB(2, dummy="b")

# You can create multiple memoisations of the same function,
# and they'll be independent.
memA(2)
memA2 <- memoise(a)
memA(2)  # Still the same outcome
memA2(2) # Different cache, different outcome

# Multiple memoized functions can share a cache.
cm <- cachem::cache_mem(max_size = 50 * 1024^2)
memA <- memoise(a, cache = cm)
memB <- memoise(b, cache = cm)

# Don't do the same memoisation assignment twice: a brand-new
# memoised function also means a brand-new cache, and *that*
# you could as easily and more legibly achieve using forget().
# (If you're not sure whether you already memoised something,
#  use is.memoised() to check.)
memA(2)
memA <- memoise(a)
memA(2)

# Make a memoized result automatically time out after 10 seconds.
memA3 <- memoise(a, cache = cachem::cache_mem(max_age = 10))
memA3(2)