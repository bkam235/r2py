# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: names2.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 17

suppressPackageStartupMessages(library(rlang))
names2(letters)

# It also takes care of standardising missing names:
x <- set_names(1:3, c("a", NA, "b"))
names2(x)

# Replacing names with the base `names<-` function may introduce
# `NA` values when the vector is unnamed:
x <- 1:3
names(x)[1:2] <- "foo"
names(x)

# Use the `names2<-` variant to avoid this
x <- 1:3
names2(x)[1:2] <- "foo"
names(x)