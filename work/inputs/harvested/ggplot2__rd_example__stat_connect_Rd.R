# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: stat_connect.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 13

suppressPackageStartupMessages(library(ggplot2))
ggplot(head(economics, 20), aes(date, unemploy)) +
  stat_connect(connection = "hv")

# Setup custom connections
x <- seq(0, 1, length.out = 20)[-1]
smooth <- cbind(x, scales::rescale(1 / (1 + exp(-(x * 10 - 5)))))
zigzag <- cbind(c(0.4, 0.6, 1), c(0.75, 0.25, 1))

ggplot(head(economics, 10), aes(date, unemploy)) +
  geom_point() +
  stat_connect(aes(colour = "zigzag"), connection = zigzag) +
  stat_connect(aes(colour = "smooth"), connection = smooth)