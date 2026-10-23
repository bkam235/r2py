# r2py crawler metadata
# package: rmarkdown
# source_type: rd_example
# topic: includes.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rmarkdown\help
# lines: 5

library(rmarkdown)

html_document(includes = includes(before_body = "header.htm"))

pdf_document(includes = includes(after_body = "footer.tex"))