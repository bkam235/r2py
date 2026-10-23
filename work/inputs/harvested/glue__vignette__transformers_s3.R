# r2py crawler metadata
# package: glue
# source_type: vignette
# topic: transformers_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glue\doc\transformers.R
# lines: 22

suppressPackageStartupMessages(library(glue))
collapse_transformer <- function(regex = "[*]$", ...) {
  function(text, envir) {
    collapse <- grepl(regex, text)
    if (collapse) {
      text <- sub(regex, "", text)
    }
    res <- identity_transformer(text, envir)
    if (collapse) {
      glue_collapse(res, ...)  
    } else {
      res
    }
  }
}

glue("{1:5*}\n{letters[1:5]*}", .transformer = collapse_transformer(sep = ", "))

glue("{1:5*}\n{letters[1:5]*}", .transformer = collapse_transformer(sep = ", ", last = " and "))

x <- c("one", "two")
glue("{x}: {1:5*}", .transformer = collapse_transformer(sep = ", "))