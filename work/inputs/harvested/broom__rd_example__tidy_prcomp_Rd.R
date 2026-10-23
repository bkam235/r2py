# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: tidy.prcomp.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 37

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed(c("maps", "ggplot2"))) withAutoprint({ # examplesIf

pc <- prcomp(USArrests, scale = TRUE)

# information about rotation
tidy(pc)

# information about samples (states)
tidy(pc, "samples")

# information about PCs
tidy(pc, "pcs")

# state map
library(dplyr)
library(ggplot2)
library(maps)

pc |>
  tidy(matrix = "samples") |>
  mutate(region = tolower(row)) |>
  inner_join(map_data("state"), by = "region") |>
  ggplot(aes(long, lat, group = group, fill = value)) +
  geom_polygon() +
  facet_wrap(~PC) +
  theme_void() +
  ggtitle("Principal components of arrest data")

au <- augment(pc, data = USArrests)

au

ggplot(au, aes(.fittedPC1, .fittedPC2)) +
  geom_point() +
  geom_text(aes(label = .rownames), vjust = 1, hjust = 1)
}) # examplesIf