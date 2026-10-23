# r2py crawler metadata
# package: knitr
# source_type: vignette
# topic: knit_print_chunk9
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\doc\knit_print.Rmd
# lines: 12

suppressPackageStartupMessages(library(knitr))
# pseudo code
knit_print.ggvis = function(x, ...) {
  res = ggvis::print_this_object(x)
  knitr::asis_output(res, meta = list(
    ggvis = list(
      version = '0.1.0',
      js  = system.file('www', 'js',  'ggvis.js',  package = 'ggvis'),
      css = system.file('www', 'www', 'ggvis.css', package = 'ggvis')
    )
  ))
}