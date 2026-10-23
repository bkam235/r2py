# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: fortify.map.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 14

suppressPackageStartupMessages(library(ggplot2))
if (require("maps")) {
ca <- map("county", "ca", plot = FALSE, fill = TRUE)
head(fortify(ca))
ggplot(ca, aes(long, lat)) +
  geom_polygon(aes(group = group))
}

if (require("maps")) {
tx <- map("county", "texas", plot = FALSE, fill = TRUE)
head(fortify(tx))
ggplot(tx, aes(long, lat)) +
  geom_polygon(aes(group = group), colour = "white")
}