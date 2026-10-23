# r2py crawler metadata
# package: curl
# source_type: vignette
# topic: intro_s1
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\curl\doc\intro.R
# lines: 7

knitr::opts_chunk$set(comment = "")
options(width = 120, max.print = 100)
wrap.simpleError <- function(x, options) {
  paste0("```\n## Error: ", x$message, "\n```")
}
library(curl)
library(jsonlite)