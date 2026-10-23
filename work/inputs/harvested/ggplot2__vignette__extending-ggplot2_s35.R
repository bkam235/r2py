# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: extending-ggplot2_s35
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\extending-ggplot2.R
# lines: 8

suppressPackageStartupMessages(library(ggplot2))
p <- ggplot(mpg, aes(displ, hwy, colour = drv)) +
  geom_point() +
  scale_colour_discrete(
    labels = c("4-wheel drive", "front wheel drive", "rear wheel drive")
  )

get_guide_data(p, "colour")