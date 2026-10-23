# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: storms.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 14

suppressPackageStartupMessages(library(dplyr))
storms

# Show a few recent storm paths
if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)
  storms |>
    filter(year >= 2000) |>
    ggplot(aes(long, lat, color = paste(year, name))) +
    geom_path(show.legend = FALSE) +
    facet_wrap(~year)
}

storms