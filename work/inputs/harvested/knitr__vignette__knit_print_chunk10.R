# r2py crawler metadata
# package: knitr
# source_type: vignette
# topic: knit_print_chunk10
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\doc\knit_print.Rmd
# lines: 8

library(knitr)
knit_print.foo = function(x, ...) {
  res = paste('> **This is a `foo` object**:', x)
  asis_output(res, meta = list(
    js  = system.file('www', 'shared', 'shiny.js',  package = 'shiny'),
    css = system.file('www', 'shared', 'shiny.css', package = 'shiny')
  ))
}