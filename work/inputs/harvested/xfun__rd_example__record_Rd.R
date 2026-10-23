# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: record.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 14

suppressPackageStartupMessages(library(xfun))
code = c("# a warning test", "1:2 + 1:3", "par(mar = c(4, 4, 1, .2))",
    "barplot(5:1, col = 2:6, horiz = TRUE)", "head(iris)",
    "sunflowerplot(iris[, 3:4], seg.col = 'purple')",
    "if (TRUE) {\n  message('Hello, xfun::record()!')\n}",
    "# throw an error", "1 + 'a'")
res = xfun::record(code, dev.args = list(width = 9, height = 6.75),
    error = TRUE)
xfun::tree(res)
format(res)
# find and clean up plot files
plots = Filter(function(x) inherits(x, "record_plot"),
    res)
file.remove(unlist(plots))