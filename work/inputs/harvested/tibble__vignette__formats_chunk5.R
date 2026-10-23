# r2py crawler metadata
# package: tibble
# source_type: vignette
# topic: formats_chunk5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tibble\doc\formats.Rmd
# lines: 9

suppressPackageStartupMessages(library(tibble))
#| echo: false
vec_ptype_abbr.formattable <- function(x, ...) {
  "dbl:fmt"
}

pillar_shaft.formattable <- function(x, ...) {
  pillar::new_pillar_shaft_simple(format(x), align = "right")
}