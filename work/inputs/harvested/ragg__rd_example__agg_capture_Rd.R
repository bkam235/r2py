# r2py crawler metadata
# package: ragg
# source_type: rd_example
# topic: agg_capture.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ragg\help
# lines: 14

suppressPackageStartupMessages(library(ragg))
cap <- agg_capture()
plot(1:10, 1:10)

# Get the plot as a matrix
raster <- cap()

# Get the plot as a nativeRaster
raster_n <- cap(native = TRUE)

dev.off()

# Look at the output
plot(as.raster(raster))