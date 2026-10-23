# r2py crawler metadata
# package: knitr
# source_type: rd_example
# topic: opts_hooks.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\help
# lines: 10

suppressPackageStartupMessages(library(knitr))
# make sure the figure width is no smaller than fig.height
opts_hooks$set(fig.width = function(options) {
    if (options$fig.width < options$fig.height) {
        options$fig.width = options$fig.height
    }
    options
})
# remove all hooks
opts_hooks$restore()