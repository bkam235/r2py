# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: vec_as_location.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 15

suppressPackageStartupMessages(library(vctrs))
x <- array(1:6, c(2, 3))
dimnames(x) <- list(c("r1", "r2"), c("c1", "c2", "c3"))

# The most common use case validates row indices
vec_as_location(1, vec_size(x))

# Negative indices can be used to index from the back
vec_as_location(-1, vec_size(x))

# Character vectors can be used if `names` are provided
vec_as_location("r2", vec_size(x), rownames(x))

# You can also construct an index for dimensions other than the first
vec_as_location(c("c2", "c1"), ncol(x), colnames(x))