# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: guide_colourbar.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 67

suppressPackageStartupMessages(library(ggplot2))
df <- expand.grid(X1 = 1:10, X2 = 1:10)
df$value <- df$X1 * df$X2

p1 <- ggplot(df, aes(X1, X2)) + geom_tile(aes(fill = value))
p2 <- p1 + geom_point(aes(size = value))

# Basic form
p1 + scale_fill_continuous(guide = "colourbar")
p1 + scale_fill_continuous(guide = guide_colourbar())
p1 + guides(fill = guide_colourbar())

# Control styles

# bar size
p1 + guides(fill = guide_colourbar(theme = theme(
  legend.key.width  = unit(0.5, "lines"),
  legend.key.height = unit(10, "lines")
)))


# no label
p1 + guides(fill = guide_colourbar(theme = theme(
  legend.text = element_blank()
)))

# no tick marks
p1 + guides(fill = guide_colourbar(theme = theme(
  legend.ticks = element_blank()
)))

# label position
p1 + guides(fill = guide_colourbar(theme = theme(
  legend.text.position = "left"
)))

# label theme
p1 + guides(fill = guide_colourbar(theme = theme(
  legend.text = element_text(colour = "blue", angle = 0)
)))

# small number of bins
p1 + guides(fill = guide_colourbar(nbin = 3))

# large number of bins
p1 + guides(fill = guide_colourbar(nbin = 100))

# make top- and bottom-most ticks invisible
p1 +
  scale_fill_continuous(
    limits = c(0,20), breaks = c(0, 5, 10, 15, 20),
    guide = guide_colourbar(nbin = 100, draw.ulim = FALSE, draw.llim = FALSE)
  )

# guides can be controlled independently
p2 +
  scale_fill_continuous(guide = "colourbar") +
  scale_size(guide = "legend")
p2 + guides(fill = "colourbar", size = "legend")

p2 +
  scale_fill_continuous(guide = guide_colourbar(theme = theme(
    legend.direction = "horizontal"
  ))) +
  scale_size(guide = guide_legend(theme = theme(
    legend.direction = "vertical"
  )))