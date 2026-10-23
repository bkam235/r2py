# r2py crawler metadata
# package: glue
# source_type: vignette
# topic: transformers_s10
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glue\doc\transformers.R
# lines: 16

suppressPackageStartupMessages(library(glue))
vv_transformer <- function(text, envir) {
  regex <- "=$"
  if (!grepl(regex, text)) {
    return(identity_transformer(text, envir))
  }

  text <- sub(regex, "", text)
  res <- identity_transformer(text, envir)
  n <- length(res)
  res <- glue_collapse(res, sep = ", ")
  if (n > 1) {
    res <- c("[", res, "]")
  }
  glue_collapse(c(text, " = ", res))
}