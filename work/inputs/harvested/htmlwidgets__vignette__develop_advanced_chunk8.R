# r2py crawler metadata
# package: htmlwidgets
# source_type: vignette
# topic: develop_advanced_chunk8
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\htmlwidgets\doc\develop_advanced.Rmd
# lines: 8

suppressPackageStartupMessages(library(htmlwidgets))
fooWidget <- function(data, name, ...) {
      # ... process the data ...
      params <- list(foo = data, bar = TRUE)
      # customize the JSON serializer
      attr(params, 'TOJSON_FUNC') <- MY_OWN_JSON_FUNCTION
      htmlwidgets::createWidget(name, x = params, ...)
    }