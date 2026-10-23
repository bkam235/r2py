# r2py crawler metadata
# package: zip
# source_type: rd_example
# topic: zip.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\zip\help
# lines: 18

suppressPackageStartupMessages(library(zip))
## Some files to zip up. We will run all this in the R session's
## temporary directory, to avoid messing up the user's workspace.
dir.create(tmp <- tempfile())
dir.create(file.path(tmp, "mydir"))
cat("first file", file = file.path(tmp, "mydir", "file1"))
cat("second file", file = file.path(tmp, "mydir", "file2"))

zipfile <- tempfile(fileext = ".zip")
zip::zip(zipfile, "mydir", root = tmp)

## List contents
zip_list(zipfile)

## Add another file
cat("third file", file = file.path(tmp, "mydir", "file3"))
zip_append(zipfile, file.path("mydir", "file3"), root = tmp)
zip_list(zipfile)