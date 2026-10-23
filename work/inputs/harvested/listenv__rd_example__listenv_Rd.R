# r2py crawler metadata
# package: listenv
# source_type: rd_example
# topic: listenv.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\listenv\help
# lines: 10

suppressPackageStartupMessages(library(listenv))
x <- listenv(c = 2, a = 3, d = "hello")
print(names(x))
names(x)[2] <- "A"
x$b <- 5:8

y <- as.list(x)
str(y)

z <- as.listenv(y)