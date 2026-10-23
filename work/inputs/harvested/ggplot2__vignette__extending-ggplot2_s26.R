# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: extending-ggplot2_s26
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\extending-ggplot2.R
# lines: 14

suppressPackageStartupMessages(library(ggplot2))
#| label: axis-line-ex
#| fig.alt:
#| - "Scatterplot of three observations arranged diagonally. The axis titles 'x' 
#|  and 'y' are coloured in black"
#| - "Scatterplot of three observations arranged diagonally. The axis titles 'x' 
#|  and 'y' are coloured in red"
df <- data.frame(x = 1:3, y = 1:3)
base <- ggplot(df, aes(x, y)) + 
  geom_point() + 
  theme_minimal()

base
base + theme(text = element_text(colour = "red"))