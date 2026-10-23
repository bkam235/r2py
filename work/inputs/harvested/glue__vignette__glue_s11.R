# r2py crawler metadata
# package: glue
# source_type: vignette
# topic: glue_s11
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glue\doc\glue.R
# lines: 11

suppressPackageStartupMessages(library(glue))
x <- glue('
  abc
  "	}

  xyz')
class(x)

x
unclass(x)
as.character(x)