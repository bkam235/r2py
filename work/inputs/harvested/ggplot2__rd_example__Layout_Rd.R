# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: Layout.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 7

suppressPackageStartupMessages(library(ggplot2))
# Some dummy layout components
facet <- facet_null()
coord <- coord_cartesian()

# Use in custom `ggplot_build()` methods
layout <- ggproto(NULL, Layout, facet = facet, coord = coord)