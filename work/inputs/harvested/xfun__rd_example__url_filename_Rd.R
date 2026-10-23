# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: url_filename.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 7

suppressPackageStartupMessages(library(xfun))
xfun::url_filename("https://yihui.org/images/logo.png")
xfun::url_filename("https://yihui.org/index.html")
xfun::url_filename("https://yihui.org/index.html?foo=bar")
xfun::url_filename("https://yihui.org/index.html#about")
xfun::url_filename("https://yihui.org")
xfun::url_filename("https://yihui.org/")