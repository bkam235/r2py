# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: tree.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 12

suppressPackageStartupMessages(library(xfun))
fit = lsfit(1:9, 1:9)
str(fit)
xfun::tree(fit)

fit = lm(dist ~ speed, data = cars)
str(fit)
xfun::tree(fit)

# some trivial examples
xfun::tree(1:10)
xfun::tree(iris)