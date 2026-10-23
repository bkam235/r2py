# r2py crawler metadata
# package: rstudioapi
# source_type: vignette
# topic: r-session_chunk4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rstudioapi\doc\r-session.Rmd
# lines: 5

suppressPackageStartupMessages(library(rstudioapi))
setHook("rstudio.sessionInit", function(newSession) {
  if (newSession)
    message("Welcome to RStudio ", rstudioapi::getVersion())
}, action = "append")