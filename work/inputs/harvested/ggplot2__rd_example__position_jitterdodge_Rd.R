# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: position_jitterdodge.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 6

suppressPackageStartupMessages(library(ggplot2))
set.seed(596)
dsub <- diamonds[sample(nrow(diamonds), 1000), ]
ggplot(dsub, aes(x = cut, y = carat, fill = clarity)) +
  geom_boxplot(outlier.size = 0) +
  geom_point(pch = 21, position = position_jitterdodge())