# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: ggplot2_s6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\ggplot2.R
# lines: 7

suppressPackageStartupMessages(library(ggplot2))
#| label: example_scales
#| fig.alt: "A scatterplot showing city versus highway miles per gallon for 
#|  many cars. The points are coloured according to seven classes of cars."
ggplot(mpg, aes(cty, hwy, colour = class)) +
  geom_point() +
  scale_colour_viridis_d()