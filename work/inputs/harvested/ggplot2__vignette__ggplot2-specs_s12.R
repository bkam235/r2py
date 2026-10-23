# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: ggplot2-specs_s12
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\ggplot2-specs.R
# lines: 11

suppressPackageStartupMessages(library(ggplot2))
#| fig.alt: "A 3-by-3 grid of text on top of points, with horizontal text
#|  justification increasing from 0 to 1 on the x-axis and vertical
#|  justification increasing from 0 to 1 on the y-axis. The points make it
#|  easier to see the relative placement of text."
just <- expand.grid(hjust = c(0, 0.5, 1), vjust = c(0, 0.5, 1))
just$label <- paste0(just$hjust, ", ", just$vjust)

ggplot(just, aes(hjust, vjust)) +
  geom_point(colour = "grey70", size = 5) +
  geom_text(aes(label = label, hjust = hjust, vjust = vjust))