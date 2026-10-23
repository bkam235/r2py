# r2py crawler metadata
# package: xtable
# source_type: vignette
# topic: xtableGallery_s33
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xtable\doc\xtableGallery.R
# lines: 6

suppressPackageStartupMessages(library(xtable))
mat <- round(matrix(c(0.9, 0.89, 200, 0.045, 2.0), c(1, 5)), 4)
rownames(mat) <- "$y_{t-1}$"
colnames(mat) <- c("$R^2$", "$\\bar{x}$", "F-stat", "S.E.E", "DW")
mat <- xtable(mat)
print(mat, sanitize.text.function = function(x) {x})