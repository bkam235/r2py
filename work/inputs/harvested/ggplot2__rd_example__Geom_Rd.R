# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: Geom.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 29

suppressPackageStartupMessages(library(ggplot2))
# Extending the class
GeomSimplePoint <- ggproto(
  "GeomSimplePoint", Geom,
  # Fields
  required_aes = c("x", "y"),
  draw_key     = draw_key_point,
  # Methods
  draw_panel = function(data, panel_params, coord) {
    data <- coord$transform(data, panel_params)
    grid::pointsGrob(data$x, data$y)
  }
)

# Building a constructor
geom_simple_point <- function(mapping = NULL, data = NULL, stat = "identity",
                              position = "identity", ..., na.rm = FALSE,
                              show.legend = NA, inherit.aes = TRUE) {
  layer(
    mapping = mapping, data = data,
    geom = GeomSimplePoint, stat = stat, position = position,
    show.legend = show.legend, inherit.aes = inherit.aes,
    params = list(na.rm = na.rm, ...)
  )
}

# Use new geom in plot
ggplot(mpg, aes(displ, hwy)) +
  geom_simple_point()