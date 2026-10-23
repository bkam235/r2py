# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: tabset.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 17

suppressPackageStartupMessages(library(xfun))
xfun::tabset(iris)
xfun::tabset(iris, dput)
xfun::tabset(iris, print)

# a deeply nested list
plot(1:10)
p = recordPlot()
xfun::tabset(p)

# custom tab content
xfun::tabset(iris, function(x) {
    if (is.factor(x)) {
        res = c("A factor with levels: ", xfun::join_words(levels(x), before = "`"))
        xfun::tab_content(res)
    } else print(summary(x))
})