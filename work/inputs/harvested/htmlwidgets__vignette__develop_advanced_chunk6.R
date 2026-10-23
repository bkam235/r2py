# r2py crawler metadata
# package: htmlwidgets
# source_type: vignette
# topic: develop_advanced_chunk6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\htmlwidgets\doc\develop_advanced.Rmd
# lines: 8

suppressPackageStartupMessages(library(htmlwidgets))
fooWidget <- function(data, name, ..., JSONArgs = list(digits = 7)) {
      # ... process the data ...
      params <- list(foo = data, bar = TRUE)
      # customize toJSON() argument values
      attr(params, 'TOJSON_ARGS') <- JSONArgs
      htmlwidgets::createWidget(name, x = params, ...)
    }