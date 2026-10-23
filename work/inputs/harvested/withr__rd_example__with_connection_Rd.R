# r2py crawler metadata
# package: withr
# source_type: rd_example
# topic: with_connection.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\withr\help
# lines: 11

suppressPackageStartupMessages(library(withr))
with_connection(list(con = file("foo", "w")), {
  writeLines(c("foo", "bar"), con)
})

read_foo <- function() {
  readLines(local_connection(file("foo", "r")))
}
read_foo()

unlink("foo")