# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: sf_transform_xy.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 16

suppressPackageStartupMessages(library(ggplot2))
if (requireNamespace("sf", quietly = TRUE)) {
# location of cities in NC by long (x) and lat (y)
data <- data.frame(
  city = c("Charlotte", "Raleigh", "Greensboro"),
  x =  c(-80.843, -78.639, -79.792),
  y = c(35.227, 35.772, 36.073)
)

# transform to projected coordinates
data_proj <- sf_transform_xy(data, 3347, 4326)
data_proj

# transform back
sf_transform_xy(data_proj, 4326, 3347)
}