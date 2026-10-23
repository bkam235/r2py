# r2py crawler metadata
# package: rvest
# source_type: rd_example
# topic: html_children.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rvest\help
# lines: 8

suppressPackageStartupMessages(library(rvest))
html <- minimal_html("<ul><li>1<li>2<li>3</ul>")
ul <- html_elements(html, "ul")
html_children(ul)

html <- minimal_html("<p>Hello <b>Hadley</b><i>!</i>")
p <- html_elements(html, "p")
html_children(p)