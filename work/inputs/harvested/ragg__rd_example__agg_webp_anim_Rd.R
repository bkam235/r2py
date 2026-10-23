# r2py crawler metadata
# package: ragg
# source_type: rd_example
# topic: agg_webp_anim.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ragg\help
# lines: 8

suppressPackageStartupMessages(library(ragg))
file <- tempfile(fileext = '.webp')
agg_webp_anim(file, delay = 100, loop = 0)
for(i in 1:10) {
  plot(sin(1:100 + i/10), type = 'l', ylim = c(-1, 1))
  dev.flush()
}
dev.off()