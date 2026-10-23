# r2py crawler metadata
# package: knitr
# source_type: vignette
# topic: knit_print_chunk4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\doc\knit_print.Rmd
# lines: 8

library(knitr)
# define a method for objects of the class data.frame
knit_print.data.frame = function(x, ...) {
  res = paste(c('', '', kable(x)), collapse = '\n')
  asis_output(res)
}
# register the method
registerS3method("knit_print", "data.frame", knit_print.data.frame)