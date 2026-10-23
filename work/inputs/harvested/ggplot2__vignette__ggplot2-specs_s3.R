# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: ggplot2-specs_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\ggplot2-specs.R
# lines: 15

suppressPackageStartupMessages(library(ggplot2))
#| fig.alt: "A series of 6 horizontal lines with different line types.
#|  From top-to-bottom they are titled 'solid', 'dashed', 'dotted',
#|  'dotdash', 'longdash', 'twodash'."
lty <- c("solid", "dashed", "dotted", "dotdash", "longdash", "twodash")
linetypes <- data.frame(
  y = seq_along(lty),
  lty = lty
)
ggplot(linetypes, aes(0, y)) +
  geom_segment(aes(xend = 5, yend = y, linetype = lty)) +
  scale_linetype_identity() +
  geom_text(aes(label = lty), hjust = 0, nudge_y = 0.2) +
  scale_x_continuous(NULL, breaks = NULL) +
  scale_y_reverse(NULL, breaks = NULL)