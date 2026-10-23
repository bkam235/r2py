# r2py crawler metadata
# package: rprojroot
# source_type: vignette
# topic: rprojroot_chunk31
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rprojroot\doc\rprojroot.Rmd
# lines: 7

suppressPackageStartupMessages(library(rprojroot))
## saved to tests/testthat/helper.R
get_my_path <- function(file_name) {
  rprojroot::find_testthat_root_file(
    "testing_data", filename
  )
}