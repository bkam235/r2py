# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: html_tag.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 7

suppressPackageStartupMessages(library(xfun))
xfun::html_tag("a", "<R Project>", href = "https://www.r-project.org", target = "_blank")
xfun::html_tag("br")
xfun::html_tag("a", xfun::html_tag("strong", "R Project"), href = "#")
xfun::html_tag("a", list("<text>", xfun::html_tag("b", "R Project")), href = "#")
xfun::html_escape("\" quotes \" & brackets < >")
xfun::html_escape("\" & < > \r \n", attr = TRUE)