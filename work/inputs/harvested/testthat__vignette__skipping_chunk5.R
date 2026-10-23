# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: skipping_chunk5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\skipping.Rmd
# lines: 16

suppressPackageStartupMessages(library(testthat))
convert_markdown_to_html <- function(in_path, out_path, ...) {
  if (rmarkdown::pandoc_available("2.0")) {
    from <- "markdown+gfm_auto_identifiers-citations+emoji+autolink_bare_uris"
  } else if (rmarkdown::pandoc_available("1.12.3")) {
    from <- "markdown_github-hard_line_breaks+tex_math_dollars+tex_math_single_backslash+header_attributes"
  } else {
    if (is_testing()) {
      testthat::skip("Pandoc not available")
    } else {
      abort("Pandoc not available")
    }
  }
  
  ...
}