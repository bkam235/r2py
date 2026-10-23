# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: zero_range.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 22

suppressPackageStartupMessages(library(scales))
eps <- .Machine$double.eps
zero_range(c(1, 1 + eps))
zero_range(c(1, 1 + 99 * eps))
zero_range(c(1, 1 + 1001 * eps))
zero_range(c(1, 1 + 2 * eps), tol = eps)

# Scaling up or down all the values has no effect since the values
# are rescaled to 1 before checking against tol
zero_range(100000 * c(1, 1 + eps))
zero_range(100000 * c(1, 1 + 1001 * eps))
zero_range(.00001 * c(1, 1 + eps))
zero_range(.00001 * c(1, 1 + 1001 * eps))

# NA values
zero_range(c(1, NA)) # NA
zero_range(c(1, NaN)) # NA

# Infinite values
zero_range(c(1, Inf)) # FALSE
zero_range(c(-Inf, Inf)) # FALSE
zero_range(c(Inf, Inf)) # TRUE