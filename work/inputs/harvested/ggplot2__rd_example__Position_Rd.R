# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: Position.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 28

suppressPackageStartupMessages(library(ggplot2))
# Extending the class
PositionRank <- ggproto(
  "PositionRank", Position,
  # Fields
  required_aes = c("x", "y"),
  # Methods
  setup_params = function(self, data) list(width = self$width),
  compute_panel = function(data, params, scales) {
    width <- params$width
    if (is.null(width)) {
      width <- resolution(data$x, zero = FALSE, TRUE) * 0.4
    }
    rank   <- stats::ave(data$y, data$group, FUN = rank)
    rank   <- scales::rescale(rank, to = c(-width, width) / 2)
    data$x <- data$x + rank
    data
  }
)

# Building a constructor
position_rank <- function(width = NULL) {
  ggproto(NULL, PositionRank, width = width)
}

# Use new position in plot
ggplot(mpg, aes(drv, displ)) +
  geom_point(position = position_rank(width = 0.5))