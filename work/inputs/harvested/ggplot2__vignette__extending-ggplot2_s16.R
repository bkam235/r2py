# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: extending-ggplot2_s16
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\extending-ggplot2.R
# lines: 24

suppressPackageStartupMessages(library(ggplot2))
#| label: GeomSimplePoint
#| fig.alt: "Scatterplot of engine displacement versus highway miles per
#|  gallon, for 234 cars. The points are larger than the default."
GeomSimplePoint <- ggproto("GeomSimplePoint", Geom,
  required_aes = c("x", "y"),
  default_aes = aes(shape = 19, colour = "black"),
  draw_key = draw_key_point,

  draw_panel = function(data, panel_params, coord) {
    coords <- coord$transform(data, panel_params)
    grid::pointsGrob(
      coords$x, coords$y,
      pch = coords$shape,
      gp = grid::gpar(col = coords$colour)
    )
  }
)

# Default stat is `stat_identity()`, no need to specify
geom_simple_point <- make_constructor(GeomSimplePoint)

ggplot(mpg, aes(displ, hwy)) + 
  geom_simple_point()