# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: ggplot2_s1
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\ggplot2.R
# lines: 15

#| label: cake
#| echo: false
#| fig.alt: "Scatterplot of city versus highway miles per gallon, for many cars
#|  coloured by engine displacement. The plot has six panels in a 2-row, 
#|  3-column layout, showing the combinations of three types of drive train and
#|  year of manifacture. Every panel has an individual trendline."
library(ggplot2)
ggplot(mpg, aes(cty, hwy)) +
  geom_point(aes(colour = displ)) +
  geom_smooth(formula = y ~ x, method = "lm") +
  scale_colour_viridis_c() +
  facet_grid(year ~ drv) +
  coord_fixed() +
  theme_minimal() +
  theme(panel.grid.minor = element_blank())