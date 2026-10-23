# r2py crawler metadata
# package: knitr
# source_type: rd_example
# topic: knit_filter.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\help
# lines: 10

library(knitr)
knitr_example = function(...) system.file("examples", ..., package = "knitr")

if (Sys.which("aspell") != "") {
    # -t means the TeX mode
    utils::aspell(knitr_example("knitr-minimal.Rnw"), knit_filter, control = "-t")

    # -H is the HTML mode
    utils::aspell(knitr_example("knitr-minimal.Rmd"), knit_filter, control = "-H -t")
}