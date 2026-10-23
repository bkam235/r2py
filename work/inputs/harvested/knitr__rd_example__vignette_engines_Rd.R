# r2py crawler metadata
# package: knitr
# source_type: rd_example
# topic: vignette_engines.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\help
# lines: 6

library(knitr)
vig_list = tools::vignetteEngine(package = "knitr")
str(vig_list)
vig_list[["knitr::knitr"]][c("weave", "tangle")]
vig_list[["knitr::knitr_notangle"]][c("weave", "tangle")]
vig_list[["knitr::docco_classic"]][c("weave", "tangle")]