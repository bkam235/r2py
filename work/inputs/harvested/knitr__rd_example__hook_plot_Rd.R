# r2py crawler metadata
# package: knitr
# source_type: rd_example
# topic: hook_plot.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\help
# lines: 14

suppressPackageStartupMessages(library(knitr))
# this is what happens for a chunk like this

# <<foo-bar-plot, dev='pdf', fig.align='right'>>=
hook_plot_tex("foo-bar-plot.pdf", opts_chunk$merge(list(fig.align = "right")))

# <<bar, dev='tikz'>>=
hook_plot_tex("bar.tikz", opts_chunk$merge(list(dev = "tikz")))

# <<foo, dev='pdf', fig.show='animate', interval=.1>>=

# 5 plots are generated in this chunk
hook_plot_tex("foo5.pdf", opts_chunk$merge(list(fig.show = "animate", interval = 0.1,
    fig.cur = 5, fig.num = 5)))