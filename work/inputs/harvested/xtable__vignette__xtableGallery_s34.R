# r2py crawler metadata
# package: xtable
# source_type: vignette
# topic: xtableGallery_s34
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xtable\doc\xtableGallery.R
# lines: 6

suppressPackageStartupMessages(library(xtable))
money <- matrix(c("$1,000","$900","$100"), ncol = 3,
                dimnames = list("$\\alpha$",
                                c("Income (US$)","Expenses (US$)",
                                  "Profit (US$)")))
print(xtable(money), sanitize.rownames.function = function(x) {x})