# r2py crawler metadata
# package: withr
# source_type: rd_example
# topic: with_par.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\withr\help
# lines: 12

suppressPackageStartupMessages(library(withr))
old <- par("col" = "black")

# This will be in red
with_par(list(col = "red", pch = 19),
  plot(mtcars$hp, mtcars$wt)
)

# This will still be in black
plot(mtcars$hp, mtcars$wt)

par(old)