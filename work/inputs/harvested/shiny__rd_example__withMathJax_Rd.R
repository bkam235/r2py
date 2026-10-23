# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: withMathJax.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 4

suppressPackageStartupMessages(library(shiny))
withMathJax(helpText("Some math here $$\\alpha+\\beta$$"))
# now we can just write "static" content without withMathJax()
div("more math here $$\\sqrt{2}$$")