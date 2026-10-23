# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: base64_encode.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 5

suppressPackageStartupMessages(library(xfun))
xfun::base64_encode(as.raw(1:10))
logo = xfun:::R_logo()
xfun::base64_encode(logo)
xfun::base64_decode("AQIDBAUGBwgJCg==")