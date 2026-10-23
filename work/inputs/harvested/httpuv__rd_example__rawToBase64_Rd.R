# r2py crawler metadata
# package: httpuv
# source_type: rd_example
# topic: rawToBase64.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httpuv\help
# lines: 4

suppressPackageStartupMessages(library(httpuv))
set.seed(100)
result <- rawToBase64(as.raw(runif(19, min=0, max=256)))
stopifnot(identical(result, "TkGNDnd7z16LK5/hR2bDqzRbXA=="))