# r2py crawler metadata
# package: testthat
# source_type: rd_example
# topic: local_mocked_s3_method.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\help
# lines: 8

suppressPackageStartupMessages(library(testthat))
x <- as.POSIXlt(Sys.time())
local({
  local_mocked_s3_method("length", "POSIXlt", function(x) 42)
  length(x)
})

length(x)