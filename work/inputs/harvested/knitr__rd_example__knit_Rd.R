# r2py crawler metadata
# package: knitr
# source_type: rd_example
# topic: knit.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\help
# lines: 9

library(knitr)
(f = system.file("examples", "knitr-minimal.Rnw", package = "knitr"))
knit(f)  # compile to tex

purl(f)  # tangle R code
purl(f, documentation = 0)  # extract R code only
purl(f, documentation = 2)  # also include documentation

unlink(c("knitr-minimal.tex", "knitr-minimal.R", "figure"), recursive = TRUE)