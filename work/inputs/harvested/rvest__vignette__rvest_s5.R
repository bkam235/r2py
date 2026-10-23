# r2py crawler metadata
# package: rvest
# source_type: vignette
# topic: rvest_s5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rvest\doc\rvest.R
# lines: 6

suppressPackageStartupMessages(library(rvest))
html <- minimal_html("
  <h1>This is a heading</h1>
  <p id='first'>This is a paragraph</p>
  <p class='important'>This is an important paragraph</p>
")