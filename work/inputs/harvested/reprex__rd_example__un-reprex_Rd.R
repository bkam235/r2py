# r2py crawler metadata
# package: reprex
# source_type: rd_example
# topic: un-reprex.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\reprex\help
# lines: 45

suppressPackageStartupMessages(library(reprex))
# a roundtrip: R code --> rendered reprex, as gfm --> R code
original <- file.path(tempdir(), "original.R")
writeLines(glue::glue("
  #' Some text
  #+ chunk-label-and-options-cannot-be-recovered, message = TRUE
  (x <- 1:4)
  #' More text
  y <- 2:5
  x + y"), con = original)
reprex(input = original, html_preview = FALSE, advertise = FALSE)
reprexed <- sub("[.]R$", "_reprex.md", original)
writeLines(readLines(reprexed))
unreprexed <- reprex_invert(input = reprexed)
writeLines(unreprexed)

# clean up
file.remove(
  list.files(dirname(original), pattern = "original", full.names = TRUE)
)


# a roundtrip: R code --> rendered reprex, as R code --> original R code
code_in <- c(
  "# a regular comment, which is retained",
  "(x <- 1:4)",
  "median(x)"
)
reprexed <- reprex(input = code_in, venue = "r", advertise = FALSE)
writeLines(reprexed)
code_out <- reprex_clean(input = reprexed)
writeLines(code_out)
identical(code_in, code_out)


# rescue a reprex that was copied from a live R session
from_r_console <- c(
  "> # a regular comment, which is retained",
  "> (x <- 1:4)",
  "[1] 1 2 3 4",
  "> median(x)",
  "[1] 2.5"
)
rescued <- reprex_rescue(input = from_r_console)
writeLines(rescued)