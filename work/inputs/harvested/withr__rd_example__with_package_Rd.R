# r2py crawler metadata
# package: withr
# source_type: rd_example
# topic: with_package.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\withr\help
# lines: 4

suppressPackageStartupMessages(library(withr))
with_package("ggplot2", {
  ggplot(mtcars) + geom_point(aes(wt, hp))
})