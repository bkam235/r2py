# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: ggplot2-specs_s6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\ggplot2-specs.R
# lines: 24

suppressPackageStartupMessages(library(ggplot2))
#| out-width: 30%
#| fig-show: hold
#| fig.alt:
#| - "A plot showing a thin red line on top of a thick black line shaped like
#|  the letter 'V'. The corner in the black V-shape is rounded."
#| - "A plot showing a thin red line on top of a thick black line shaped like
#|  the letter 'V'. The corner in the black V-shape is sharp."
#| - "A plot showing a thin red line on top of a thick black line shaped like
#|  the letter 'V'. A piece of the corner is cut off so that the two
#|  straight parts are connected by a horizontal part."
df <- data.frame(x = 1:3, y = c(9, 1, 9))
base <- ggplot(df, aes(x, y)) + ylim(0, 10)
base +
  geom_path(linewidth = 10) +
  geom_path(linewidth = 1, colour = "red")

base +
  geom_path(linewidth = 10, linejoin = "mitre") +
  geom_path(linewidth = 1, colour = "red")

base +
  geom_path(linewidth = 10, linejoin = "bevel") +
  geom_path(linewidth = 1, colour = "red")