# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: protect_math.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 4

library(xfun)
protect_math(c("hi $a+b$", "hello $$\\alpha$$", "no math here: $x is $10 dollars"))
protect_math(c("hi $$", "\\begin{equation}", "x + y = z", "\\end{equation}"))
protect_math("$a+b$", "===")