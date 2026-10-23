# r2py crawler metadata
# package: readr
# source_type: rd_example
# topic: parse_factor.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readr\help
# lines: 20

suppressPackageStartupMessages(library(readr))
# discover the levels from the data
parse_factor(c("a", "b"))
parse_factor(c("a", "b", "-99"))
parse_factor(c("a", "b", "-99"), na = c("", "NA", "-99"))
parse_factor(c("a", "b", "-99"), na = c("", "NA", "-99"), include_na = FALSE)

# provide the levels explicitly
parse_factor(c("a", "b"), levels = letters[1:5])

x <- c("cat", "dog", "caw")
animals <- c("cat", "dog", "cow")

# base::factor() silently converts elements that do not match any levels to
# NA
factor(x, levels = animals)

# parse_factor() generates same factor as base::factor() but throws a warning
# and reports problems
parse_factor(x, levels = animals)