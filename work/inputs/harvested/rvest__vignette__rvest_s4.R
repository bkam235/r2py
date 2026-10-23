# r2py crawler metadata
# package: rvest
# source_type: vignette
# topic: rvest_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rvest\doc\rvest.R
# lines: 8

suppressPackageStartupMessages(library(rvest))
html <- minimal_html("
  <p>This is a paragraph<p>
  <ul>
    <li>This is a bulleted list</li>
  </ul>
")
html