# r2py crawler metadata
# package: ragg
# source_type: rd_example
# topic: agg_tiff.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ragg\help
# lines: 6

suppressPackageStartupMessages(library(ragg))
file <- tempfile(fileext = '.tiff')
# Use jpeg compression
agg_tiff(file, compression = 'lzw+p')
plot(sin, -pi, 2*pi)
dev.off()