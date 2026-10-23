# r2py crawler metadata
# package: xfun
# source_type: vignette
# topic: xfun_chunk7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\doc\xfun.Rmd
# lines: 5

library(xfun)
f = tempfile()
writeLines(c("hello", "world"), f)
gsub_file(f, "world", "woRld", fixed = TRUE)
file_string(f)