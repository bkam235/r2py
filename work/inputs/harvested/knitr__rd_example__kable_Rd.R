# r2py crawler metadata
# package: knitr
# source_type: rd_example
# topic: kable.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\help
# lines: 40

suppressPackageStartupMessages(library(knitr))
d1 = head(iris)
d2 = head(mtcars)
# pipe tables by default
kable(d1)
kable(d2[, 1:5])
# no inner padding
kable(d2, format = "pipe", padding = 0)
# more padding
kable(d2, format = "pipe", padding = 2)
kable(d1, format = "latex")
kable(d1, format = "html")
kable(d1, format = "latex", caption = "Title of the table")
kable(d1, format = "html", caption = "Title of the table")
# use the booktabs package
kable(mtcars, format = "latex", booktabs = TRUE)
# use the longtable package
kable(matrix(1000, ncol = 5), format = "latex", digits = 2, longtable = TRUE)
# change LaTeX default table environment
kable(d1, format = "latex", caption = "My table", table.envir = "table*")
# add some table attributes
kable(d1, format = "html", table.attr = "id=\"mytable\"")
# reST output
kable(d2, format = "rst")
# no row names
kable(d2, format = "rst", row.names = FALSE)
# Pandoc simple tables
kable(d2, format = "simple", caption = "Title of the table")
# format numbers using , as decimal point, and ' as thousands separator
x = as.data.frame(matrix(rnorm(60, 1e+06, 10000), 10))
kable(x, format.args = list(decimal.mark = ",", big.mark = "'"))
# save the value
x = kable(d2, format = "html")
cat(x, sep = "\n")
# can also set options(knitr.table.format = 'html') so that the output is HTML

# multiple tables via either kable(list(x1, x2)) or kables(list(kable(x1),
# kable(x2)))
kable(list(d1, d2), caption = "A tale of two tables")
kables(list(kable(d1, align = "l"), kable(d2)), caption = "A tale of two tables")