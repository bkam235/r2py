# r2py crawler metadata
# package: htmltools
# source_type: rd_example
# topic: tagQuery.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\htmltools\help
# lines: 6

suppressPackageStartupMessages(library(htmltools))
tagQ <- tagQuery(div(a()))
tagQ$find("a")$addClass("foo")
tagQ

# To learn more, visit https://rstudio.github.io/htmltools/articles/tagQuery.html