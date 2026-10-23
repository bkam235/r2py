# r2py crawler metadata
# package: xtable
# source_type: vignette
# topic: xtableGallery_s16
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xtable\doc\xtableGallery.R
# lines: 5

suppressPackageStartupMessages(library(xtable))
temp.ts <- ts(cumsum(1 + round(rnorm(100), 0)),
              start = c(1954, 7), frequency = 12)
temp.table <- xtable(temp.ts, digits = 0)
temp.table