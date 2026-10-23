# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: new_continuous_palette.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 32

suppressPackageStartupMessages(library(scales))
# Creating a new discrete palette
new_discrete_palette(
  fun = grDevices::terrain.colors,
  type = "colour", nlevels = 255
)

# Creating a new continuous palette
new_continuous_palette(
  fun = function(x) rescale(x, to = c(1, 0)),
  type = "numeric", na_safe = FALSE
)

# Testing palette properties
is_continuous_pal(pal_seq_gradient())
is_discrete_pal(pal_viridis())
is_numeric_pal(pal_area())
is_colour_pal(pal_manual(c("red", "green")))
is_pal(transform_log10())

# Extracting properties
palette_nlevels(pal_viridis())
palette_na_safe(colour_ramp(c("red", "green"), na.color = "grey50"))
palette_type(pal_shape())

# Switching discrete to continuous
pal <- as_continuous_pal(pal_viridis())
show_col(pal(c(0, 0.1, 0.2, 0.4, 1)))

# Switching continuous to discrete
pal <- as_discrete_pal(pal_div_gradient())
show_col(pal(9))