# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: benchplot.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 7

suppressPackageStartupMessages(library(ggplot2))
benchplot(ggplot(mtcars, aes(mpg, wt)) + geom_point())
benchplot(ggplot(mtcars, aes(mpg, wt)) + geom_point() + facet_grid(. ~ cyl))

# With tidy eval:
p <- expr(ggplot(mtcars, aes(mpg, wt)) + geom_point())
benchplot(!!p)