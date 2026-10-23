# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: extending-ggplot2_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\extending-ggplot2.R
# lines: 9

suppressPackageStartupMessages(library(ggplot2))
#| label: chull
StatChull <- ggproto("StatChull", Stat,
  compute_group = function(data, scales) {
    data[chull(data$x, data$y), , drop = FALSE]
  },
  
  required_aes = c("x", "y")
)