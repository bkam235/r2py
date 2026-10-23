# r2py crawler metadata
# package: knitr
# source_type: rd_example
# topic: output_type.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\help
# lines: 10

suppressPackageStartupMessages(library(knitr))
# check for output formats type
knitr::is_latex_output()
knitr::is_html_output()
knitr::is_html_output(excludes = c("markdown", "epub"))
# Get current formats
knitr::pandoc_from()
knitr::pandoc_to()
# Test if current output format is 'docx'
knitr::pandoc_to("docx")