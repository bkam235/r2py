# r2py crawler metadata
# package: rmarkdown
# source_type: vignette
# topic: lua-filters_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rmarkdown\doc\lua-filters.R
# lines: 11

suppressPackageStartupMessages(library(rmarkdown))
custom_format <- function(...) {
  base_format <- rmarkdown::html_document(...)
  # prepending a new Lua filter to html_document() ones
  base_format$pandoc$lua_filters <- c(
    rmarkdown::pandoc_path_arg("new.lua"), 
    base_format$pandoc$lua_filters)
  base_format
}

basename(custom_format()$pandoc$lua_filters)