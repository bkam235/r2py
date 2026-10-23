# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: base64_uri.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 4

suppressPackageStartupMessages(library(xfun))
logo = xfun:::R_logo()
img = xfun::html_tag("img", src = xfun::base64_uri(logo), alt = "R logo")
if (interactive()) xfun::html_view(img)