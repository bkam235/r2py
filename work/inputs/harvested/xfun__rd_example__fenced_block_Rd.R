# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: fenced_block.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 9

suppressPackageStartupMessages(library(xfun))
# code block with class 'r' and ID 'foo'
xfun::fenced_block("1+1", c(".r", "#foo"))
# fenced Div
xfun::fenced_block("This is a **Div**.", char = ":")
# three backticks by default
xfun::make_fence("1+1")
# needs five backticks for the fences because content has four
xfun::make_fence(c("````r", "1+1", "````"))