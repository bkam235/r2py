# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: scale_binned.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 5

suppressPackageStartupMessages(library(ggplot2))
# Create a histogram by binning the x-axis
ggplot(mtcars) +
  geom_bar(aes(mpg)) +
  scale_x_binned()