# r2py crawler metadata
# package: readxl
# source_type: rd_example
# topic: excel_format.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readxl\help
# lines: 10

suppressPackageStartupMessages(library(readxl))
files <- c(
  "a.xlsx",
  "b.xls",
  "c.png",
  file.path(R.home("doc"), "html", "logo.jpg"),
  readxl_example("clippy.xlsx"),
  readxl_example("deaths.xls")
)
excel_format(files)