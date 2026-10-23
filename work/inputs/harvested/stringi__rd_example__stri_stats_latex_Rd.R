# r2py crawler metadata
# package: stringi
# source_type: rd_example
# topic: stri_stats_latex.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringi\help
# lines: 5

suppressPackageStartupMessages(library(stringi))
s <- c('Lorem \\textbf{ipsum} dolor sit \\textit{amet}, consectetur adipisicing elit.',
       '\\begin{small}Proin nibh augue,\\end{small} suscipit a, scelerisque sed, lacinia in, mi.',
       '')
stri_stats_latex(s)