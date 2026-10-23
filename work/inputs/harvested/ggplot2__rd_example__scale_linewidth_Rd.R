# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: scale_linewidth.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 9

suppressPackageStartupMessages(library(ggplot2))
p <- ggplot(economics, aes(date, unemploy, linewidth = uempmed)) +
  geom_line(lineend = "round")
p
p + scale_linewidth("Duration of\nunemployment")
p + scale_linewidth(range = c(0, 4))

# Binning can sometimes make it easier to match the scaled data to the legend
p + scale_linewidth_binned()