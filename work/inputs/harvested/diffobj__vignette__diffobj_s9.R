# r2py crawler metadata
# package: diffobj
# source_type: vignette
# topic: diffobj_s9
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\diffobj\doc\diffobj.R
# lines: 4

suppressPackageStartupMessages(library(diffobj))
mdl1 <- lm(Sepal.Length ~ Sepal.Width, iris)
mdl2 <- lm(Sepal.Length ~ Sepal.Width + Species, iris)
diffStr(mdl1$qr, mdl2$qr, line.limit=15)