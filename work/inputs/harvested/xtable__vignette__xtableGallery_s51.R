# r2py crawler metadata
# package: xtable
# source_type: vignette
# topic: xtableGallery_s51
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xtable\doc\xtableGallery.R
# lines: 4

suppressPackageStartupMessages(library(xtable))
bktbs <- xtable(matrix(1:10, ncol = 2))
hlines <- c(-1, 0, 1, nrow(bktbs))
print(bktbs, booktabs = TRUE, hline.after = hlines)