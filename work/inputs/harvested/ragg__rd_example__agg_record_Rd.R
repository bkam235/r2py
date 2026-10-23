# r2py crawler metadata
# package: ragg
# source_type: rd_example
# topic: agg_record.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ragg\help
# lines: 12

suppressPackageStartupMessages(library(ragg))
# Capture drawing instructions
agg_record()
plot(1:10, 1:10)
rec <- recordPlot()
dev.off()

# Replay these on another device
file <- tempfile(fileext = '.png')
agg_png(file)
replayPlot(rec)
dev.off()