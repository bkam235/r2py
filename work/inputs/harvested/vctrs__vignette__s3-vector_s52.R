# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: s3-vector_s52
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\s3-vector.R
# lines: 39

suppressPackageStartupMessages(library(vctrs))
poly <- function(...) {
  x <- vec_cast_common(..., .to = integer())
  new_poly(x)
}
new_poly <- function(x) {
  new_list_of(x, ptype = integer(), class = "vctrs_poly_list")
}

vec_ptype_full.vctrs_poly_list <- function(x, ...) "polynomial"
vec_ptype_abbr.vctrs_poly_list <- function(x, ...) "poly"

format.vctrs_poly_list <- function(x, ...) {
  format_one <- function(x) {
    if (length(x) == 0) {
      return("")
    }

    if (length(x) == 1) {
      format(x)
    } else {
      suffix <- c(paste0("\u22C5x^", seq(length(x) - 1, 1)), "")
      out <- paste0(x, suffix)
      out <- out[x != 0L]
      paste0(out, collapse = " + ")
    }
  }

  vapply(x, format_one, character(1))
}

obj_print_data.vctrs_poly_list <- function(x, ...) {
  if (length(x) != 0) {
    print(format(x), quote = FALSE)
  }
}

p <- poly(1, c(1, 0, 0, 0, 2), c(1, 0, 1))
p