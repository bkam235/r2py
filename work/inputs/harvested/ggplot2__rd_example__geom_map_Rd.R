# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: geom_map.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 72

suppressPackageStartupMessages(library(ggplot2))
# First, a made-up example containing a few polygons, to explain
# how `geom_map()` works. It requires two data frames:
# One contains the coordinates of each polygon (`positions`), and is
# provided via the `map` argument. The other contains the
# values associated with each polygon (`values`).  An id
# variable links the two together.

ids <- factor(c("1.1", "2.1", "1.2", "2.2", "1.3", "2.3"))

values <- data.frame(
  id = ids,
  value = c(3, 3.1, 3.1, 3.2, 3.15, 3.5)
)

positions <- data.frame(
  id = rep(ids, each = 4),
  x = c(2, 1, 1.1, 2.2, 1, 0, 0.3, 1.1, 2.2, 1.1, 1.2, 2.5, 1.1, 0.3,
  0.5, 1.2, 2.5, 1.2, 1.3, 2.7, 1.2, 0.5, 0.6, 1.3),
  y = c(-0.5, 0, 1, 0.5, 0, 0.5, 1.5, 1, 0.5, 1, 2.1, 1.7, 1, 1.5,
  2.2, 2.1, 1.7, 2.1, 3.2, 2.8, 2.1, 2.2, 3.3, 3.2)
)

ggplot(values) +
  geom_map(aes(map_id = id), map = positions) +
  expand_limits(positions)
ggplot(values, aes(fill = value)) +
  geom_map(aes(map_id = id), map = positions) +
  expand_limits(positions)
ggplot(values, aes(fill = value)) +
  geom_map(aes(map_id = id), map = positions) +
  expand_limits(positions) + ylim(0, 3)

# Now some examples with real maps
if (require(maps)) {

  crimes <- data.frame(state = tolower(rownames(USArrests)), USArrests)

  # Equivalent to crimes |> tidyr::pivot_longer(Murder:Rape)
  vars <- lapply(names(crimes)[-1], function(j) {
    data.frame(state = crimes$state, variable = j, value = crimes[[j]])
  })
  crimes_long <- do.call("rbind", vars)

  states_map <- map_data("state")

  # without geospatial coordinate system, the resulting plot
  # looks weird
  ggplot(crimes, aes(map_id = state)) +
    geom_map(aes(fill = Murder), map = states_map) +
    expand_limits(x = states_map$long, y = states_map$lat)

  # in combination with `coord_sf()` we get an appropriate result
  ggplot(crimes, aes(map_id = state)) +
    geom_map(aes(fill = Murder), map = states_map) +
    # crs = 5070 is a Conus Albers projection for North America,
    #   see: https://epsg.io/5070
    # default_crs = 4326 tells coord_sf() that the input map data
    #   are in longitude-latitude format
    coord_sf(
      crs = 5070, default_crs = 4326,
      xlim = c(-125, -70), ylim = c(25, 52)
    )

 ggplot(crimes_long, aes(map_id = state)) +
   geom_map(aes(fill = value), map = states_map) +
   coord_sf(
     crs = 5070, default_crs = 4326,
     xlim = c(-125, -70), ylim = c(25, 52)
   ) +
   facet_wrap(~variable)
}