# r2py crawler metadata
# package: listenv
# source_type: rd_example
# topic: aperm.listenv.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\listenv\help
# lines: 11

suppressPackageStartupMessages(library(listenv))
x <- as.listenv(1:6)
dim(x) <- c(2, 3)
dimnames(x) <- list(letters[1:2], LETTERS[1:3])
print(x)

x <- t(x)
print(x)

x <- aperm(x, perm = 2:1)
print(x)