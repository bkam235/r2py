# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: ggplot2-specs_s7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\ggplot2-specs.R
# lines: 16

suppressPackageStartupMessages(library(ggplot2))
#| fig.alt: "A 5-by-5 grid of point symbols annotated by the numbers
#|  that can be used to represent the symbols. From left to right, the
#|  first 15 symbols are lines or open shapes, the next 5 symbols are solid
#|  shapes and the last 5 symbols are filled shaped."
shapes <- data.frame(
  shape = c(0:19, 22, 21, 24, 23, 20),
  x = 0:24 %/% 5,
  y = -(0:24 %% 5)
)
ggplot(shapes, aes(x, y)) +
  geom_point(aes(shape = shape), size = 5, fill = "red") +
  geom_text(aes(label = shape), hjust = 0, nudge_x = 0.15) +
  scale_shape_identity() +
  expand_limits(x = 4.1) +
  theme_void()