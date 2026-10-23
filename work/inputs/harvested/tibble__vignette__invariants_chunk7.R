# r2py crawler metadata
# package: tibble
# source_type: vignette
# topic: invariants_chunk7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tibble\doc\invariants.Rmd
# lines: 48

suppressPackageStartupMessages(library(tibble))
#| label: with-def
#| include: false
with_df <- function(code, verbose = FALSE) {
  code <- rlang::enexpr(code)

  full_code <- rlang::quo({
    df <- new_df()
    !!code
    df
  })
  if (verbose) rlang::expr_print(rlang::quo_get_expr(full_code))
  rlang::eval_tidy(full_code)
}

with_tbl <- function(code, verbose = FALSE) {
  code <- rlang::enexpr(code)

  full_code <- rlang::quo({
    tbl <- new_tbl()
    !!code
    tbl
  })
  if (verbose) rlang::expr_print(rlang::quo_get_expr(full_code))
  rlang::eval_tidy(full_code)
}

with_df2 <- function(code) {
  code <- rlang::enexpr(code)

  full_code <- rlang::quo({
    df2 <- new_df2()
    !!code
    df2
  })
  rlang::eval_tidy(full_code)
}

with_tbl2 <- function(code) {
  code <- rlang::enexpr(code)

  full_code <- rlang::quo({
    tbl2 <- new_tbl2()
    !!code
    tbl2
  })
  rlang::eval_tidy(full_code)
}