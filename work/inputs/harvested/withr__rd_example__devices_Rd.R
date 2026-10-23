# r2py crawler metadata
# package: withr
# source_type: rd_example
# topic: devices.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\withr\help
# lines: 10

suppressPackageStartupMessages(library(withr))
# dimensions are in inches
with_pdf(file.path(tempdir(), "test.pdf"), width = 7, height = 5,
  plot(runif(5))
)

# dimensions are in pixels
with_png(file.path(tempdir(), "test.png"), width = 800, height = 600,
  plot(runif(5))
)