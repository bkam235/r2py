# r2py crawler metadata
# package: knitr
# source_type: vignette
# topic: knit_print_chunk14
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\doc\knit_print.Rmd
# lines: 7

suppressPackageStartupMessages(library(knitr))
knit_print.bar = function(x, ...) {
  asis_output(x, meta = list(head = '<script>console.log("bar!")</script>'))
}
new_bar = function(x) structure(x, class = 'bar')
new_bar('> **hello** world!')
new_bar('> hello **world**!')