# r2py crawler metadata
# package: withr
# source_type: rd_example
# topic: with_makevars.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\withr\help
# lines: 5

suppressPackageStartupMessages(library(withr))
writeLines("void foo(int* bar) { *bar = 1; }\n", "foo.c")
system("R CMD SHLIB --preclean -c foo.c")
with_makevars(c(CFLAGS = "-O3"), system("R CMD SHLIB --preclean -c foo.c"))
unlink(c("foo.c", "foo.so"))