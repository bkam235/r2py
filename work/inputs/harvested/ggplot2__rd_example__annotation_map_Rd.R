# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: annotation_map.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 42

suppressPackageStartupMessages(library(ggplot2))
if (requireNamespace("maps", quietly = TRUE)) {
# location of cities in North Carolina
df <- data.frame(
  name = c("Charlotte", "Raleigh", "Greensboro"),
  lat = c(35.227, 35.772, 36.073),
  long = c(-80.843, -78.639, -79.792)
)

p <- ggplot(df, aes(x = long, y = lat)) +
  annotation_map(
    map_data("state"),
    fill = "antiquewhite", colour = "darkgrey"
  ) +
  geom_point(color = "blue") +
  geom_text(
    aes(label = name),
    hjust = 1.105, vjust = 1.05, color = "blue"
  )

# use without coord_sf() is possible but not recommended
p + xlim(-84, -76) + ylim(34, 37.2)

if (requireNamespace("sf", quietly = TRUE)) {
# use with coord_sf() for appropriate projection
p +
  coord_sf(
    crs = sf::st_crs(3347),
    default_crs = sf::st_crs(4326),  # data is provided as long-lat
    xlim = c(-84, -76),
    ylim = c(34, 37.2)
  )

# you can mix annotation_map() and geom_sf()
nc <- sf::st_read(system.file("shape/nc.shp", package = "sf"), quiet = TRUE)
p +
  geom_sf(
    data = nc, inherit.aes = FALSE,
    fill = NA, color = "black", linewidth = 0.1
  ) +
  coord_sf(crs = sf::st_crs(3347), default_crs = sf::st_crs(4326))
}}