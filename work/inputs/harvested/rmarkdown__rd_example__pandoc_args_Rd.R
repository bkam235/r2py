# r2py crawler metadata
# package: rmarkdown
# source_type: rd_example
# topic: pandoc_args.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rmarkdown\help
# lines: 10

library(rmarkdown)

pandoc_include_args(before_body = "header.htm")
pandoc_include_args(before_body = "header.tex")

pandoc_highlight_args("kate")

pandoc_latex_engine_args("pdflatex")

pandoc_toc_args(toc = TRUE, toc_depth = 2)