# r2py crawler metadata
# package: zip
# source_type: rd_example
# topic: zip_process.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\zip\help
# lines: 8

suppressPackageStartupMessages(library(zip))
dir.create(tmp <- tempfile())
write.table(iris, file = file.path(tmp, "iris.ssv"))
zipfile <- tempfile(fileext = ".zip")
zp <- zip_process()$new(zipfile, tmp)
zp$wait()
zp$get_exit_status()
zip_list(zipfile)