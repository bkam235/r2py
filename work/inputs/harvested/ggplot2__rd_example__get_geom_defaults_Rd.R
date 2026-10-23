# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: get_geom_defaults.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 15

suppressPackageStartupMessages(library(ggplot2))
# Using a function
get_geom_defaults(geom_raster)

# Using a layer includes static aesthetics as default
get_geom_defaults(geom_tile(fill = "white"))

# Using a class name
get_geom_defaults("density_2d")

# Using a class
get_geom_defaults(GeomPoint)

# Changed theme
get_geom_defaults("point", theme(geom = element_geom(ink = "purple")))