# r2py crawler metadata
# package: knitr
# source_type: rd_example
# topic: Sweave2knitr.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\help
# lines: 12

suppressPackageStartupMessages(library(knitr))
Sweave2knitr(text = "<<echo=TRUE>>=")  # this is valid
Sweave2knitr(text = "<<png=true>>=")  # dev='png'
Sweave2knitr(text = "<<eps=TRUE, pdf=FALSE, results=tex, width=5, prefix.string=foo>>=")
Sweave2knitr(text = "<<,png=false,fig=TRUE>>=")
Sweave2knitr(text = "\\SweaveOpts{echo=false}")
Sweave2knitr(text = "\\SweaveInput{hello.Rnw}")
# Sweave example in utils
testfile = system.file("Sweave", "Sweave-test-1.Rnw", package = "utils")
Sweave2knitr(testfile, output = "Sweave-test-knitr.Rnw")
if (interactive()) knit("Sweave-test-knitr.Rnw")  # or knit2pdf() directly
unlink("Sweave-test-knitr.Rnw")