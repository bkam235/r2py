# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: embed_file.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 5

suppressPackageStartupMessages(library(xfun))
logo = xfun:::R_logo()
link = xfun::embed_file(logo, text = "Download R logo")
link
if (interactive()) xfun::html_view(link)