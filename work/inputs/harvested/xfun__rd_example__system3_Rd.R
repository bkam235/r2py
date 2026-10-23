# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: system3.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 10

suppressPackageStartupMessages(library(xfun))
if (interactive()) {
a = shQuote(c("-e", "print(intToUtf8(c(20320, 22909)))"))
x2 = system2("Rscript", a, stdout = TRUE)
Encoding(x2)  # unknown

x3 = xfun::system3("Rscript", a, stdout = TRUE)
# encoding of x3 should be UTF-8 if the current locale is UTF-8
!l10n_info()[["UTF-8"]] || Encoding(x3) == "UTF-8"  # should be TRUE
}