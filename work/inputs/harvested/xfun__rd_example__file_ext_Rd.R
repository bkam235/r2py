# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: file_ext.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 12

library(xfun)
p = c("abc.doc", "def123.tex", "path/to/foo.Rmd", "backup.ppt~", "pkg.tar.xz")
file_ext(p)
sans_ext(p)
with_ext(p, ".txt")
with_ext(p, c(".ppt", ".sty", ".Rnw", "doc", "zip"))
with_ext(p, "html")

# allow for more characters in extensions
p = c("a.c++", "b.c--", "c.e##")
file_ext(p)  # -/+/# not recognized by default
file_ext(p, extra = "-+#")