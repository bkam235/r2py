# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: extending-ggplot2_s24
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\extending-ggplot2.R
# lines: 5

suppressPackageStartupMessages(library(ggplot2))
theme_grey()$legend.key

new_theme <- theme_grey() + theme(legend.key = element_rect(colour = "red"))
new_theme$legend.key