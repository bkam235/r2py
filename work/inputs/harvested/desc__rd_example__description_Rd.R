# r2py crawler metadata
# package: desc
# source_type: rd_example
# topic: description.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\desc\help
# lines: 17

suppressPackageStartupMessages(library(desc))
## Create a template
desc <- description$new("!new")
desc

## Read a file
desc2 <- description$new(file = system.file("DESCRIPTION",
                           package = "desc"))
desc2

## Remove a field
desc2$del("LazyData")

## Add another one
desc2$set(VignetteBuilder = "knitr")
desc2$get("VignetteBuilder")
desc2