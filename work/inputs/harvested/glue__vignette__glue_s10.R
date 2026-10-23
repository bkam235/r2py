# r2py crawler metadata
# package: glue
# source_type: vignette
# topic: glue_s10
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glue\doc\glue.R
# lines: 14

suppressPackageStartupMessages(library(glue))
# no leading or trailing newline
x <- glue("
  blah
  ")
unclass(x)

# both a leading and trailing newline
y <- glue("

  blah

  ")
unclass(y)