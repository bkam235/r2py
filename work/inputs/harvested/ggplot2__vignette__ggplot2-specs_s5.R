# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: ggplot2-specs_s5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\ggplot2-specs.R
# lines: 25

suppressPackageStartupMessages(library(ggplot2))
#| out-width: 30%
#| fig-show: hold
#| fig.alt:
#| - "A plot showing a line with an angle. A thinner red line is placed over
#|  a thicker black line. The black line ends where the red line ends."
#| - "A plot showing a line with an angle. A thinner red line is placed over
#|  a thicker black line. The black line ends past where the red line ends,
#|  and ends in a semicircle."
#| - "A plot showing a line with an angle. A thinner red line is placed over
#|  a thicker black line. The black line ends past where the red line ends,
#|  and ends in a square shape."
df <- data.frame(x = 1:3, y = c(4, 1, 9))
base <- ggplot(df, aes(x, y)) + xlim(0.5, 3.5) + ylim(0, 10)
base +
  geom_path(linewidth = 10) +
  geom_path(linewidth = 1, colour = "red")

base +
  geom_path(linewidth = 10, lineend = "round") +
  geom_path(linewidth = 1, colour = "red")

base +
  geom_path(linewidth = 10, lineend = "square") +
  geom_path(linewidth = 1, colour = "red")