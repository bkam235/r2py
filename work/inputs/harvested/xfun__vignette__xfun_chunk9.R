# r2py crawler metadata
# package: xfun
# source_type: vignette
# topic: xfun_chunk9
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\doc\xfun.Rmd
# lines: 7

library(xfun)
p = c("abc.doc", "def123.tex", "path/to/foo.Rmd")
file_ext(p)
sans_ext(p)
with_ext(p, ".txt")
with_ext(p, c(".ppt", ".sty", ".Rnw"))
with_ext(p, "html")