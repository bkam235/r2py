# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: vec_as_names_legacy.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 15

suppressPackageStartupMessages(library(vctrs))
if (rlang::is_installed("tibble")) {

library(tibble)

# Names repair is turned off by default in tibble:
try(tibble(a = 1, a = 2))

# You can turn it on by supplying a repair method:
tibble(a = 1, a = 2, .name_repair = "universal")

# If you prefer the legacy method, use `vec_as_names_legacy()`:
tibble(a = 1, a = 2, .name_repair = vec_as_names_legacy)

}