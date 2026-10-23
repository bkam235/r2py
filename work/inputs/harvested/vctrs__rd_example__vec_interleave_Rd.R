# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: vec_interleave.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 18

suppressPackageStartupMessages(library(vctrs))
# The most common case is to interleave two vectors
vec_interleave(1:3, 4:6)

# But you aren't restricted to just two
vec_interleave(1:3, 4:6, 7:9, 10:12)

# You can also interleave data frames
x <- data_frame(x = 1:2, y = c("a", "b"))
y <- data_frame(x = 3:4, y = c("c", "d"))

vec_interleave(x, y)

# `.size` can be used to recycle size 1 elements before interleaving
vec_interleave(1, 2, .size = 3)

# `.ptype` can be used to enforce a particular type
typeof(vec_interleave(1, 2, .ptype = integer()))