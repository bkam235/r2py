# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: Stat.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 32

suppressPackageStartupMessages(library(ggplot2))
# Extending the class
StatKmeans <- ggproto(
  "StatKmeans", Stat,
  # Fields
  required_aes = c("x", "y"),
  # You can relate computed variables to aesthetics using `after_stat()`
  # in defaults
  default_aes = aes(colour = after_stat(cluster)),
  # Methods
  compute_panel = function(data, scales, k = 2L) {
    km <- kmeans(cbind(scale(data$x), scale(data$y)), centers = k)
    data$cluster <- factor(km$cluster)
    data
  }
)

# Building a constructor
stat_kmeans <- function(mapping = NULL, data = NULL, geom = "point",
                        position = "identity", ..., k = 2L, na.rm = FALSE,
                        show.legend = NA, inherit.aes = TRUE) {
  layer(
    mapping = mapping, data = data,
    geom = geom, stat = StatKmeans, position = position,
    show.legend = show.legend, inherit.aes = inherit.aes,
    params = list(na.rm = na.rm, k = k, ...)
  )
}

# Use new stat in plot
ggplot(mpg, aes(displ, hwy)) +
  stat_kmeans(k = 3)