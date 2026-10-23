# r2py crawler metadata
# package: readr
# source_type: rd_example
# topic: read_lines.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readr\help
# lines: 12

suppressPackageStartupMessages(library(readr))
read_lines(file.path(R.home("doc"), "AUTHORS"), n_max = 10)
read_lines_raw(file.path(R.home("doc"), "AUTHORS"), n_max = 10)

tmp <- tempfile()

write_lines(rownames(mtcars), tmp)
read_lines(tmp, lazy = FALSE)
read_file(tmp) # note trailing \n

write_lines(airquality$Ozone, tmp, na = "-1")
read_lines(tmp)