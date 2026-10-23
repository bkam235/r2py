# r2py crawler metadata
# package: parallelly
# source_type: rd_example
# topic: isConnectionValid.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\parallelly\help
# lines: 23

suppressPackageStartupMessages(library(parallelly))
## R represents connections as plain indices
as.integer(stdin())          ## int 0
as.integer(stdout())         ## int 1
as.integer(stderr())         ## int 2

## The first three connections always exist and are always valid
isConnectionValid(stdin())   ## TRUE
connectionId(stdin())        ## 0L
isConnectionValid(stdout())  ## TRUE
connectionId(stdout())       ## 1L
isConnectionValid(stderr())  ## TRUE
connectionId(stderr())       ## 2L

## Connections cannot be serialized
con <- file(tempfile(), open = "w")
x <- list(value = 42, stderr = stderr(), con = con)
y <- unserialize(serialize(x, connection = NULL))
isConnectionValid(y$stderr)  ## TRUE
connectionId(y$stderr)       ##  2L
isConnectionValid(y$con)     ## FALSE with attribute 'reason'
connectionId(y$con)          ## -1L
close(con)