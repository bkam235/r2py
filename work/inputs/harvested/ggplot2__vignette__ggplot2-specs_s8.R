# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: ggplot2-specs_s8
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\ggplot2-specs.R
# lines: 29

suppressPackageStartupMessages(library(ggplot2))
#| out-width: 90%
#| fig-asp: 0.4
#| fig-width: 8
#| fig.alt: "An irregular 6-by-7 grid of point symbols annotated by the
#|  names that can be used to represent the symbols. Broadly, from top to
#|  bottom, the symbols are circles, squares, diamonds, triangles and
#|  others. Broadly from left to right, the symbols are solid shapes,
#|  open shapes, filled shapes and others."
shape_names <- c(
  "circle", paste("circle", c("open", "filled", "cross", "plus", "small")), "bullet",
  "square", paste("square", c("open", "filled", "cross", "plus", "triangle")),
  "diamond", paste("diamond", c("open", "filled", "plus")),
  "triangle", paste("triangle", c("open", "filled", "square")),
  paste("triangle down", c("open", "filled")),
  "plus", "cross", "asterisk"
)

shapes <- data.frame(
  shape_names = shape_names,
  x = c(1:7, 1:6, 1:3, 5, 1:3, 6, 2:3, 1:3),
  y = -rep(1:6, c(7, 6, 4, 4, 2, 3))
)

ggplot(shapes, aes(x, y)) +
  geom_point(aes(shape = shape_names), fill = "red", size = 5) +
  geom_text(aes(label = shape_names), nudge_y = -0.3, size = 3.5) +
  scale_shape_identity() +
  theme_void()