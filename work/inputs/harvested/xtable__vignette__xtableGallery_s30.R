# r2py crawler metadata
# package: xtable
# source_type: vignette
# topic: xtableGallery_s30
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xtable\doc\xtableGallery.R
# lines: 5

suppressPackageStartupMessages(library(xtable))
wanttex <- xtable(data.frame(Column =
                             paste("Value_is $10^{-",1:3,"}$", sep = "")))
print(wanttex, sanitize.text.function =
      function(str) gsub("_", "\\_", str, fixed = TRUE))