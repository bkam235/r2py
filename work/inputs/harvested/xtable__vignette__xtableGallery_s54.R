# r2py crawler metadata
# package: xtable
# source_type: vignette
# topic: xtableGallery_s54
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xtable\doc\xtableGallery.R
# lines: 4

suppressPackageStartupMessages(library(xtable))
x <- matrix(rnorm(1000), ncol = 10)
x.big <- xtable(x, caption = "A \\code{longtable} spanning several pages")
print(x.big, hline.after=c(-1, 0), tabular.environment = "longtable")