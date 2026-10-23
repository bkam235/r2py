# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: tidy.map.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 20

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed(c("maps", "ggplot2"))) withAutoprint({ # examplesIf

# load libraries for models and data
library(maps)
library(ggplot2)

ca <- map("county", "ca", plot = FALSE, fill = TRUE)

tidy(ca)

qplot(long, lat, data = ca, geom = "polygon", group = group)

tx <- map("county", "texas", plot = FALSE, fill = TRUE)
tidy(tx)
qplot(long, lat,
  data = tx, geom = "polygon", group = group,
  colour = I("white")
)
}) # examplesIf