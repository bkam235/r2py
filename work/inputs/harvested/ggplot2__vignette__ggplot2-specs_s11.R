# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: ggplot2-specs_s11
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\ggplot2-specs.R
# lines: 8

suppressPackageStartupMessages(library(ggplot2))
#| fig.alt: "A plot showing four text labels arranged vertically. The top
#|  label is 'bold.italic' and is displayed in bold and italic. The next three
#|  labels are 'italic', 'bold' and 'plain' and are displayed in their
#|  respective styles."
df <- data.frame(x = 1:4, fontface = c("plain", "bold", "italic", "bold.italic"))
ggplot(df, aes(1, x)) +
  geom_text(aes(label = fontface, fontface = fontface))