# r2py crawler metadata
# package: pkgdown
# source_type: rd_example
# topic: test-figures.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pkgdown\help
# lines: 9

suppressPackageStartupMessages(library(pkgdown))
x <- seq(0, 2 * pi, length.out = 25)
plot(x, sin(x))

plot(1:10)
lines(1:10)
text(2, 5, "Hello", srt = 30, cex = 2)

plot(1:3, col = c("red", "green", "blue"), pch = 16, cex = 10)