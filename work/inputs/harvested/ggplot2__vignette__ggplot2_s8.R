# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: ggplot2_s8
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\ggplot2.R
# lines: 8

suppressPackageStartupMessages(library(ggplot2))
#| label: example_coords
#| fig.alt: "A scatterplot showing city versus highway miles per gallon for 
#|  many cars. The aspect ratio of the plot is such that units on the x-axis
#|  have the same length as units on the y-axis."
ggplot(mpg, aes(cty, hwy)) +
  geom_point() +
  coord_fixed()