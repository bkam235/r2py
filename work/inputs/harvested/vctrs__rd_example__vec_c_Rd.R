# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: vec_c.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 23

suppressPackageStartupMessages(library(vctrs))
vec_c(FALSE, 1L, 1.5)

# Date/times --------------------------
c(Sys.Date(), Sys.time())
c(Sys.time(), Sys.Date())

vec_c(Sys.Date(), Sys.time())
vec_c(Sys.time(), Sys.Date())

# Factors -----------------------------
c(factor("a"), factor("b"))
vec_c(factor("a"), factor("b"))


# By default, named inputs must be length 1:
vec_c(name = 1)
try(vec_c(name = 1:3))

# Pass a name specification to work around this:
vec_c(name = 1:3, .name_spec = "{outer}_{inner}")

# See `?name_spec` for more examples of name specifications.