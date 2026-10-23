# r2py crawler metadata
# package: xtable
# source_type: vignette
# topic: xtableGallery_s61
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xtable\doc\xtableGallery.R
# lines: 5

suppressPackageStartupMessages(library(xtable))
df <- data.frame(name = c("A","B"), right = c(1.4, 34.6),
                 left = c(1.4, 34.6), text = c("txt1","txt2"))
print(xtable(df, align = c("l", "|c", "|R{3cm}", "|L{3cm}", "| p{3cm}|")),
      floating = FALSE, include.rownames = FALSE)