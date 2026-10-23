# r2py crawler metadata
# package: diffobj
# source_type: rd_example
# topic: tag_f.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\diffobj\help
# lines: 8

suppressPackageStartupMessages(library(diffobj))
## Assuming class 'ex1' has CSS styles defined elsewhere
tag_f("div", "ex1")(LETTERS[1:5])
## Use convenience function, and add some inline styles
div_f("ex2", c(color="green", `font-family`="arial"))(LETTERS[1:5])
## Notice how this is a div with pre-specifed class,
## and only one div is created around the entire data
cont_f()(LETTERS[1:5])