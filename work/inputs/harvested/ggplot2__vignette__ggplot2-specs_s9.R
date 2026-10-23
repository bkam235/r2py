# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: ggplot2-specs_s9
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\ggplot2-specs.R
# lines: 11

suppressPackageStartupMessages(library(ggplot2))
#| fig.alt: "A plot showing a 4-by-4 grid of red points, the top 12 points with
#|  black outlines. The size of the points increases horizontally. The stroke of
#|  the outlines of the points increases vertically. A white diagonal line with
#|  a negative slope marks that the 'stroke' versus 'size' trade-off has
#|  similar total sizes."
sizes <- expand.grid(size = (0:3) * 2, stroke = (0:3) * 2)
ggplot(sizes, aes(size, stroke, size = size, stroke = stroke)) +
  geom_abline(slope = -1, intercept = 6, colour = "white", linewidth = 6) +
  geom_point(shape = 21, fill = "red") +
  scale_size_identity()