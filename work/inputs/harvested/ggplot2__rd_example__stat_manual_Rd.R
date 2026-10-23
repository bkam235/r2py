# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: stat_manual.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 64

suppressPackageStartupMessages(library(ggplot2))
# A standard scatterplot
p <- ggplot(mtcars, aes(disp, mpg, colour = factor(cyl))) +
  geom_point()

# The default just displays points as-is
p + stat_manual()

# Using a custom function
make_hull <- function(data) {
  hull <- chull(x = data$x, y = data$y)
  data.frame(x = data$x[hull], y = data$y[hull])
}

p + stat_manual(
  geom = "polygon",
  fun  = make_hull,
  fill = NA
)

# Using the `with` function with quoting
p + stat_manual(
  fun  = with,
  args = list(expr = quote({
    hull <- chull(x, y)
    list(x = x[hull], y = y[hull])
  })),
  geom = "polygon", fill = NA
)

# Using the `transform` function with quoting
p + stat_manual(
  geom = "segment",
  fun  = transform,
  args = list(
    xend = quote(mean(x)),
    yend = quote(mean(y))
  )
)

# Using dplyr verbs with `vars()`
if (requireNamespace("dplyr", quietly = TRUE)) {

  # Get centroids with `summarise()`
  p + stat_manual(
    size = 10, shape = 21,
    fun  = dplyr::summarise,
    args = vars(x = mean(x), y = mean(y))
  )

  # Connect to centroid with `mutate`
  p + stat_manual(
    geom = "segment",
    fun  = dplyr::mutate,
    args = vars(xend = mean(x), yend = mean(y))
  )

  # Computing hull with `reframe()`
  p + stat_manual(
    geom = "polygon", fill = NA,
    fun  = dplyr::reframe,
    args = vars(hull = chull(x, y), x = x[hull], y = y[hull])
  )
}