# r2py crawler metadata
# package: cli
# source_type: rd_example
# topic: ansi_html.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cli\help
# lines: 17

suppressPackageStartupMessages(library(cli))
if (cli:::has_packages(c("htmltools", "withr"))) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
## Syntax highlight the source code of an R function with ANSI tags,
## and export it to a HTML file.
code <- withr::with_options(
  list(ansi.num_colors = 256),
  code_highlight(format(ansi_html))
)
hcode <- paste(ansi_html(code), collapse = "\n")
css <- paste(format(ansi_html_style()), collapse=  "\n")
page <- htmltools::tagList(
  htmltools::tags$head(htmltools::tags$style(css)),
  htmltools::tags$pre(htmltools::HTML(hcode))
)

if (interactive()) htmltools::html_print(page)
}) # examplesIf