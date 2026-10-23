# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: ggplot2_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\ggplot2.R
# lines: 31

suppressPackageStartupMessages(library(ggplot2))
#| label: overview_graphic
#| echo: false
#| fig.alt: "A schematic displaying seven overlaying rhombuses indicating the
#|  different composable parts. From bottom to top, the labels read 'Data', 
#|  'Mapping', 'Layers', 'Scales', 'Facets', 'Coordinates' and 'Theme'."
n <- 7
x <- outer(c(-2, 0, 2, 0), rep(1, n))
y <- outer(c(0, 1, 0, -1), seq(0, 2.309, length.out = n), FUN = `+`)

df <- data.frame(
  x = as.vector(x),
  y = as.vector(y),
  group = as.vector(col(x))
)

ggplot(df, aes(x, y, group = group, fill = factor(group))) +
  geom_polygon(alpha = 0.9) +
  coord_equal() +
  scale_y_continuous(
    breaks = seq(0, 2.309, length.out = n),
    labels = c("Data", "Mapping", "Layers", "Scales",
               "Facets", "Coordinates", "Theme")
  ) +
  scale_fill_manual(
    values = c("#E69F00", "#56B4E9", "#009E73", "#F0E442",
               "#0072B2", "#D55E00", "#CC79A7"),
    guide = "none"
  ) +
  theme_void() +
  theme(axis.text.y = element_text(face = "bold", hjust = 1))