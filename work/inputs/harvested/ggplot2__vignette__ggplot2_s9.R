# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: ggplot2_s9
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\ggplot2.R
# lines: 14

suppressPackageStartupMessages(library(ggplot2))
#| label: example_theme
#| fig.alt: "A scatterplot showing city versus highway miles per gallon for 
#|  many cars. The points are coloured according to seven classes of cars. The
#|  legend of the colour is displayed on top of the plot. The plot has thick
#|  axis lines and the bottom axis line is blue."
ggplot(mpg, aes(cty, hwy, colour = class)) +
  geom_point() +
  theme_minimal() +
  theme(
    legend.position = "top",
    axis.line = element_line(linewidth = 0.75),
    axis.line.x.bottom = element_line(colour = "blue")
  )