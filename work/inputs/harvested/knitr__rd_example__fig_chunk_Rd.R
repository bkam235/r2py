# r2py crawler metadata
# package: knitr
# source_type: rd_example
# topic: fig_chunk.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\help
# lines: 5

library(knitr)
fig_chunk("foo", "png")
fig_chunk("foo", "pdf")
fig_chunk("foo", "svg", 2)  # the second plot of the chunk foo
fig_chunk("foo", "png", 1:5)  # if the chunk foo produced 5 plots