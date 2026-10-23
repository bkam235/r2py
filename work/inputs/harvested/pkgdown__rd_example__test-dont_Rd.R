# r2py crawler metadata
# package: pkgdown
# source_type: rd_example
# topic: test-dont.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pkgdown\help
# lines: 57

suppressPackageStartupMessages(library(pkgdown))
# \dontrun{} --------------------------------------------------------
# always shown; never run

x <- 1
x <- 2

  x <- 3
  x <- 4

x # should be 1

# \donttest{} -------------------------------------------------------
# only multiline are shown; always run

x <- 1
x <- 2

  x <- 3
  x <- 4

x # should be 4

# \testonly{} -----------------------------------------------------
# never shown, never run

x <- 1
x <- 2

  x <- 3
  x <- 4

x # should be 1

# \dontshow{} -------------------------------------------------------
# never shown, always run

x <- 1
x <- 2

  x <- 3
  x <- 4

x # should be 4

# @examplesIf ------------------------------------------------------
# If FALSE, wrapped in if; if TRUE, not seen

x <- 1

if (FALSE) withAutoprint({ # examplesIf
x <- 2
}) # examplesIf
if (TRUE) withAutoprint({ # examplesIf
x <- 3
}) # examplesIf
x # should be 3