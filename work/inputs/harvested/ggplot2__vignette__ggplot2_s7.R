# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: ggplot2_s7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\ggplot2.R
# lines: 8

suppressPackageStartupMessages(library(ggplot2))
#| label: example_facets
#| fig.alt: "Scatterplot of city versus highway miles per gallon, for many cars.
#|  The plot has six panels in a 2-row, 3-column layout, showing the 
#|  combinations of three types of drive train and year of manifacture."
ggplot(mpg, aes(cty, hwy)) +
  geom_point() +
  facet_grid(year ~ drv)