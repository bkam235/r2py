# r2py crawler metadata
# package: xtable
# source_type: vignette
# topic: OtherPackagesGallery_s5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xtable\doc\OtherPackagesGallery.R
# lines: 8

suppressPackageStartupMessages(library(xtable))
library(survival)
test1 <- list(time=c(4,3,1,1,2,2,3),
              status=c(1,1,1,0,1,1,0),
              x=c(0,2,1,1,1,0,0),
              sex=c(0,0,0,0,1,1,1))
coxFit <- coxph(Surv(time, status) ~ x + strata(sex), test1)
xtable(coxFit)