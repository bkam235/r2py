# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: guide_legend.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 59

suppressPackageStartupMessages(library(ggplot2))
df <- expand.grid(X1 = 1:10, X2 = 1:10)
df$value <- df$X1 * df$X2

p1 <- ggplot(df, aes(X1, X2)) + geom_tile(aes(fill = value))
p2 <- p1 + geom_point(aes(size = value))

# Basic form
p1 + scale_fill_continuous(guide = guide_legend())

# Control styles

# title position
p1 + guides(fill = guide_legend(
  title = "LEFT", theme(legend.title.position = "left")
))

# title text styles via element_text
p1 + guides(fill = guide_legend(theme = theme(
  legend.title = element_text(size = 15, face = "italic", colour = "red")
)))

# label position
p1 + guides(fill = guide_legend(theme = theme(
  legend.text.position = "left",
  legend.text = element_text(hjust = 1)
)))

# label styles
p1 +
  scale_fill_continuous(
    breaks = c(5, 10, 15),
    labels = paste("long", c(5, 10, 15)),
    guide = guide_legend(theme = theme(
      legend.direction = "horizontal",
      legend.title.position = "top",
      legend.text.position = "bottom",
      legend.text = element_text(hjust = 0.5, vjust = 1, angle = 90)
    ))
  )

# Set aesthetic of legend key
# very low alpha value make it difficult to see legend key
p3 <- ggplot(mtcars, aes(vs, am, colour = factor(cyl))) +
  geom_jitter(alpha = 1/5, width = 0.01, height = 0.01)
p3
# override.aes overwrites the alpha
p3 + guides(colour = guide_legend(override.aes = list(alpha = 1)))

# multiple row/col legends
df <- data.frame(x = 1:20, y = 1:20, color = letters[1:20])
p <- ggplot(df, aes(x, y)) +
  geom_point(aes(colour = color))
p + guides(col = guide_legend(nrow = 8))
p + guides(col = guide_legend(ncol = 8))
p + guides(col = guide_legend(nrow = 8, theme = theme(legend.byrow = TRUE)))

# reversed order legend
p + guides(col = guide_legend(reverse = TRUE))