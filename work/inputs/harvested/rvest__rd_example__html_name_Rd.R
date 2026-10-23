# r2py crawler metadata
# package: rvest
# source_type: rd_example
# topic: html_name.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rvest\help
# lines: 8

suppressPackageStartupMessages(library(rvest))
url <- "https://rvest.tidyverse.org/articles/starwars.html"
html <- read_html(url)

html |>
  html_element("div") |>
  html_children() |>
  html_name()