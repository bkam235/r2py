# r2py crawler metadata
# package: xtable
# source_type: vignette
# topic: xtableGallery_s56
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xtable\doc\xtableGallery.R
# lines: 7

suppressPackageStartupMessages(library(xtable))
Grade3 <- c("A","B","B","A","B","C","C","D","A","B",
            "C","C","C","D","B","B","D","C","C","D")
Grade6 <- c("A","A","A","B","B","B","B","B","C","C",
            "A","C","C","C","D","D","D","D","D","D")
Cohort <- table(Grade3, Grade6)
Cohort