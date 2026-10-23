# r2py crawler metadata
# package: tinytex
# source_type: rd_example
# topic: tlmgr.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tinytex\help
# lines: 14

suppressPackageStartupMessages(library(tinytex))
if (interactive()) withAutoprint({ # examplesIf
# search for a package that contains titling.sty
tlmgr_search('titling.sty')

# to match titling.sty exactly, add a slash before the keyword, e.g.
tlmgr_search('/titling.sty')

# use a regular expression if you want to be more precise, e.g.
tlmgr_search('/titling\\.sty$')

# list all installed LaTeX packages
tlmgr(c('info', '--list', '--only-installed', '--data', 'name'))
}) # examplesIf