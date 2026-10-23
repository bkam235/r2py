# r2py crawler metadata
# package: knitr
# source_type: rd_example
# topic: knit_print.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\help
# lines: 10

library(knitr)
# write tables for data frames
knit_print.data.frame = function(x, ...) {
    res = paste(c("", "", kable(x, output = FALSE)), collapse = "\n")
    asis_output(res)
}
# register the method
registerS3method("knit_print", "data.frame", knit_print.data.frame)
# after you define and register the above method, data frames will be printed
# as tables in knitr, which is different with the default print() behavior