# r2py crawler metadata
# package: zip
# source_type: rd_example
# topic: unzip.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\zip\help
# lines: 17

suppressPackageStartupMessages(library(zip))
## temporary directory, to avoid messing up the user's workspace.
dir.create(tmp <- tempfile())
dir.create(file.path(tmp, "mydir"))
cat("first file", file = file.path(tmp, "mydir", "file1"))
cat("second file", file = file.path(tmp, "mydir", "file2"))

zipfile <- tempfile(fileext = ".zip")
zip::zip(zipfile, "mydir", root = tmp)

## List contents
zip_list(zipfile)

## Extract
tmp2 <- tempfile()
unzip(zipfile, exdir = tmp2)
dir(tmp2, recursive = TRUE)