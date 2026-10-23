# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: name_spec.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 29

suppressPackageStartupMessages(library(vctrs))
# By default, named inputs must be length 1:
vec_c(name = 1)         # ok
try(vec_c(name = 1:3))  # bad

# They also can't have internal names, even if scalar:
try(vec_c(name = c(internal = 1)))  # bad

# Pass a name specification to work around this. A specification
# can be a glue string referring to `outer` and `inner`:
vec_c(name = 1:3, other = 4:5, .name_spec = "{outer}")
vec_c(name = 1:3, other = 4:5, .name_spec = "{outer}_{inner}")

# They can also be functions:
my_spec <- function(outer, inner) paste(outer, inner, sep = "_")
vec_c(name = 1:3, other = 4:5, .name_spec = my_spec)

# Or purrr-style formulas for anonymous functions:
vec_c(name = 1:3, other = 4:5, .name_spec = ~ paste0(.x, .y))

# Or the string `"inner"` to only use inner names
vec_c(name = 1:3, outer = 4:5, .name_spec = "inner")
vec_c(name = c(a = 1, b = 2, c = 3), outer = 4:5, .name_spec = "inner")
# This can be useful when you want outer names mentioned in error messages,
# but you don't want them interfering with the result
try(vec_c(x = c(a = 1), y = c(b = "2"), .name_spec = "inner"))

# Or `rlang::zap()` to ignore both outer and inner names entirely
vec_c(name = c(a = 1, b = 2), outer = c(c = 3), .name_spec = rlang::zap())