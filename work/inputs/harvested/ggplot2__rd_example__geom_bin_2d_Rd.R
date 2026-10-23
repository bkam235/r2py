# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: geom_bin_2d.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 11

suppressPackageStartupMessages(library(ggplot2))
d <- ggplot(diamonds, aes(x, y)) + xlim(4, 10) + ylim(4, 10)
d + geom_bin_2d()

# You can control the size of the bins by specifying the number of
# bins in each direction:
d + geom_bin_2d(bins = 10)
d + geom_bin_2d(bins = list(x = 30, y = 10))

# Or by specifying the width of the bins
d + geom_bin_2d(binwidth = c(0.1, 0.1))