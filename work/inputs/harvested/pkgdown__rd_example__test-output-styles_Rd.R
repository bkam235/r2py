# r2py crawler metadata
# package: pkgdown
# source_type: rd_example
# topic: test-output-styles.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pkgdown\help
# lines: 15

suppressPackageStartupMessages(library(pkgdown))
# This example illustrates some important output types
# The following output should be wrapped over multiple lines
a <- 1:100
a

cat("This some text!\n")
message("This is a message!")
warning("This is a warning!")

# This is a multi-line block
{
  1 + 2
  2 + 2
}