# r2py crawler metadata
# package: ragg
# source_type: rd_example
# topic: agg_png.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ragg\help
# lines: 5

suppressPackageStartupMessages(library(ragg))
file <- tempfile(fileext = '.png')
agg_png(file)
plot(sin, -pi, 2*pi)
dev.off()