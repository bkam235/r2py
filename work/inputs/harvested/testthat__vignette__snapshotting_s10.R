# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: snapshotting_s10
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\snapshotting.R
# lines: 14

suppressPackageStartupMessages(library(testthat))
try({
bullets <- function(text, id = NULL) {
  paste0(
    "<ul", if (!is.null(id)) paste0(" id=\"", id, "\""), ">\n", 
    paste0("<li>", text, "</li>\n", collapse = ""),
    "</ul>\n"
  )
}
test_that("bullets", {
  expect_snapshot(cat(bullets("a")))
  expect_snapshot(cat(bullets("a", "b")))
})
})