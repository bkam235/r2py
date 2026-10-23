# r2py crawler metadata
# package: withr
# source_type: rd_example
# topic: with_timezone.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\withr\help
# lines: 18

suppressPackageStartupMessages(library(withr))
Sys.time()
with_timezone("Europe/Paris", print(Sys.time()))
with_timezone("America/Los_Angeles", print(Sys.time()))

fun1 <- function() {
  local_timezone("CET")
  print(Sys.time())
}

fun2 <- function() {
  local_timezone("America/Los_Angeles")
  print(Sys.time())
}
Sys.time()
fun1()
fun2()
Sys.time()