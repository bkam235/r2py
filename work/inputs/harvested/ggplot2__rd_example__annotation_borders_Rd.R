# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: annotation_borders.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 19

suppressPackageStartupMessages(library(ggplot2))
if (require("maps")) {
data(us.cities)
capitals <- subset(us.cities, capital == 2)
ggplot(capitals, aes(long, lat)) +
  annotation_borders("state") +
  geom_point(aes(size = pop)) +
  scale_size_area() +
  coord_quickmap()
}

if (require("maps")) {
# Same map, with some world context
ggplot(capitals, aes(long, lat)) +
  annotation_borders("world", xlim = c(-130, -60), ylim = c(20, 50)) +
  geom_point(aes(size = pop)) +
  scale_size_area() +
  coord_quickmap()
}