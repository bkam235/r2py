# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: cache_exec.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 18

suppressPackageStartupMessages(library(xfun))
# the first run takes about 1 second
y1 = xfun::cache_exec({
    x = rnorm(1e+05)
    Sys.sleep(1)
    x
}, path = ":memory:", id = "sim-norm")

# the second run takes almost no time
y2 = xfun::cache_exec({
    # comments won't affect caching
    x = rnorm(1e+05)
    Sys.sleep(1)
    x
}, path = ":memory:", id = "sim-norm")

# y1, y2, and x should be identical
stopifnot(identical(y1, y2), identical(y1, x))