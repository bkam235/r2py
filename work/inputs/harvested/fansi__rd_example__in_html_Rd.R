# r2py crawler metadata
# package: fansi
# source_type: rd_example
# topic: in_html.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fansi\help
# lines: 12

suppressPackageStartupMessages(library(fansi))
txt <- "\033[31;42mHello \033[7mWorld\033[m"
writeLines(txt)
html <- to_html(txt)

in_html(html) # spawns a browser window

writeLines(readLines(in_html(html, display=FALSE)))
css <- "SPAN {text-decoration: underline;}"
writeLines(readLines(in_html(html, css=css, display=FALSE)))

in_html(html, css)