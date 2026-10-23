# r2py crawler metadata
# package: glue
# source_type: vignette
# topic: glue_s8
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glue\doc\glue.R
# lines: 5

suppressPackageStartupMessages(library(glue))
release_date <- as.Date("2017-06-13")
glue("
  The first version of the glue package was released on \\
  a {format(release_date, '%A')}.")