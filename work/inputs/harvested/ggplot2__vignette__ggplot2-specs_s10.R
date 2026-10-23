# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: ggplot2-specs_s10
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\ggplot2-specs.R
# lines: 8

suppressPackageStartupMessages(library(ggplot2))
#| fig.alt: "A plot showing three text labels arranged vertically. The top
#|  label is 'sans' and is displayed in a sans-serif font. The middle label is
#|  'serif' and is displayed in a serif font. The bottom label is 'mono' and
#|  is displayed in a monospaced font."
df <- data.frame(x = 1, y = 3:1, family = c("sans", "serif", "mono"))
ggplot(df, aes(x, y)) +
  geom_text(aes(label = family, family = family))