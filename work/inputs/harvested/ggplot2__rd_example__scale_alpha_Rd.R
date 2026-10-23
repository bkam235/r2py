# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: scale_alpha.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 12

suppressPackageStartupMessages(library(ggplot2))
p <- ggplot(mpg, aes(displ, hwy)) +
  geom_point(aes(alpha = year))

# The default range of 0.1-1.0 leaves all data visible
p

# Include 0 in the range to make data invisible
p + scale_alpha(range = c(0, 1))

# Changing the title
p + scale_alpha("cylinders")