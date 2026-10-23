# r2py crawler metadata
# package: forcats
# source_type: rd_example
# topic: fct.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\forcats\help
# lines: 23

suppressPackageStartupMessages(library(forcats))
# Use factors when you know the set of possible values a variable might take
x <- c("A", "O", "O", "AB", "A")
fct(x, levels = c("O", "A", "B", "AB"))

# If you don't specify the levels, fct will create from the data
# in the order that they're seen
fct(x)


# Differences with base R -----------------------------------------------
# factor() silently generates NAs
x <- c("a", "b", "c")
factor(x, levels = c("a", "b"))
# fct() errors
try(fct(x, levels = c("a", "b")))
# Unless you explicitly supply NA:
fct(x, levels = c("a", "b"), na = "c")

# factor() sorts default levels:
factor(c("y", "x"))
# fct() uses in order of appearance:
fct(c("y", "x"))