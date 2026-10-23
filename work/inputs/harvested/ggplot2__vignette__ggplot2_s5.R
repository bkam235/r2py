# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: ggplot2_s5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\ggplot2.R
# lines: 10

suppressPackageStartupMessages(library(ggplot2))
#| label: example_layer
#| fig-show: hold
#| fig.alt: "A scatterplot showing city versus highway miles per gallon for 
#|  many cars. The plot has a blue trendline with a positive slope."
ggplot(mpg, aes(cty, hwy)) +
  # to create a scatterplot
  geom_point() +
  # to fit and overlay a loess trendline
  geom_smooth(formula = y ~ x, method = "lm")