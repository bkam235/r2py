# r2py crawler metadata
# package: xtable
# source_type: vignette
# topic: xtableGallery_s28
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xtable\doc\xtableGallery.R
# lines: 7

suppressPackageStartupMessages(library(xtable))
print(xtable(data.frame(text = c("foo","bar"),
                        googols = c(10e10,50e10),
                        small = c(8e-24,7e-5),
                        row.names = c("A","B")),
             display = c("s","s","g","g")),
      math.style.exponents = TRUE)