# r2py crawler metadata
# package: rvest
# source_type: vignette
# topic: rvest_s7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rvest\doc\rvest.R
# lines: 11

suppressPackageStartupMessages(library(rvest))
html <- minimal_html("
  <ol>
    <li>apple &amp; pear</li>
    <li>banana</li>
    <li>pineapple</li>
  </ol>
")
html |> 
  html_elements("li") |> 
  html_text2()