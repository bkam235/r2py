# r2py crawler metadata
# package: rvest
# source_type: vignette
# topic: rvest_s12
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rvest\doc\rvest.R
# lines: 5

suppressPackageStartupMessages(library(rvest))
html <- minimal_html("
  <p><a href='https://en.wikipedia.org/wiki/Cat'>cats</a></p>
  <img src='https://cataas.com/cat' width='100' height='200'>
")