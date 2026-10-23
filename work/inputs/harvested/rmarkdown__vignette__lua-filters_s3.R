# r2py crawler metadata
# package: rmarkdown
# source_type: vignette
# topic: lua-filters_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rmarkdown\doc\lua-filters.R
# lines: 11

suppressPackageStartupMessages(library(rmarkdown))
custom_format <- function(toc = TRUE, ...) {
  rmarkdown::output_format(
    knitr = rmarkdown::knitr_options(),
    # a new filter will be appended to base_format ones
    pandoc = rmarkdown::pandoc_options(to = "html", lua_filters = "new.lua"),
    base_format = rmarkdown::html_document(toc = toc, ...)
  )
}

basename(custom_format()$pandoc$lua_filters)