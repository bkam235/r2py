# r2py crawler metadata
# package: plyr
# source_type: rd_example
# topic: splitter_d.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\plyr\help
# lines: 13

suppressPackageStartupMessages(library(plyr))
plyr:::splitter_d(mtcars, .(cyl))
plyr:::splitter_d(mtcars, .(vs, am))
plyr:::splitter_d(mtcars, .(am, vs))

mtcars$cyl2 <- factor(mtcars$cyl, levels = c(2, 4, 6, 8, 10))
plyr:::splitter_d(mtcars, .(cyl2), drop = TRUE)
plyr:::splitter_d(mtcars, .(cyl2), drop = FALSE)

mtcars$cyl3 <- ifelse(mtcars$vs == 1, NA, mtcars$cyl)
plyr:::splitter_d(mtcars, .(cyl3))
plyr:::splitter_d(mtcars, .(cyl3, vs))
plyr:::splitter_d(mtcars, .(cyl3, vs), drop = FALSE)