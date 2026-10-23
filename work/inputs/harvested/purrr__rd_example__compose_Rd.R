# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: compose.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 18

suppressPackageStartupMessages(library(purrr))
not_null <- compose(`!`, is.null)
not_null(4)
not_null(NULL)

add1 <- function(x) x + 1
compose(add1, add1)(8)

fn <- compose(\(x) paste(x, "foo"), \(x) paste(x, "bar"))
fn("input")

# Lists of functions can be spliced with !!!
fns <- list(
  function(x) paste(x, "foo"),
  \(x) paste(x, "bar")
)
fn <- compose(!!!fns)
fn("input")