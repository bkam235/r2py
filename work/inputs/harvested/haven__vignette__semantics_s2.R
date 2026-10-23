# r2py crawler metadata
# package: haven
# source_type: vignette
# topic: semantics_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\haven\doc\semantics.R
# lines: 12

suppressPackageStartupMessages(library(haven))
x1 <- labelled(
  sample(1:5), 
  c(Good = 1, Bad = 5)
)
x1

x2 <- labelled(
  c("M", "F", "F", "F", "M"), 
  c(Male = "M", Female = "F")
)
x2