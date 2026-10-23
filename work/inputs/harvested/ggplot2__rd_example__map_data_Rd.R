# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: map_data.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 19

suppressPackageStartupMessages(library(ggplot2))
if (require("maps")) {
states <- map_data("state")
arrests <- USArrests
names(arrests) <- tolower(names(arrests))
arrests$region <- tolower(rownames(USArrests))

choro <- merge(states, arrests, sort = FALSE, by = "region")
choro <- choro[order(choro$order), ]
ggplot(choro, aes(long, lat)) +
  geom_polygon(aes(group = group, fill = assault)) +
  coord_map("albers",  lat0 = 45.5, lat1 = 29.5)
}

if (require("maps")) {
ggplot(choro, aes(long, lat)) +
  geom_polygon(aes(group = group, fill = assault / murder)) +
  coord_map("albers",  lat0 = 45.5, lat1 = 29.5)
}