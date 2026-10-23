# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: Coord.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 32

suppressPackageStartupMessages(library(ggplot2))
# Extending the class
CoordJitter <- ggproto(
  "CoordJitter", CoordCartesian,
  # Fields
  amount = 0,
  # Methods
  is_linear = function() FALSE,
  transform = function(self, data, panel_params) {
    data   <- ggproto_parent(CoordCartesian, self)$transform(data, panel_params)
    data$x <- jitter(data$x, amount = self$amount)
    data$y <- jitter(data$y, amount = self$amount)
    data
  }
)

# Building a constructor
coord_jitter <- function(amount = 0.005, xlim = NULL, ylim = NULL, expand = TRUE,
                         clip = "on", reverse = "none") {
  ggproto(
    NULL, CoordJitter,
    amount = amount,
    limits = list(x = xlim, y = ylim),
    reverse = reverse, expand = expand, clip = clip
  )
}

# Use new coord in plot
set.seed(42)
ggplot(mpg, aes(drv, displ)) +
  geom_boxplot() +
  coord_jitter()