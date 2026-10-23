# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: type-size_s33
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\type-size.R
# lines: 19

suppressPackageStartupMessages(library(vctrs))
try({
# length-0 output
1:2 + integer()
atan2(1:2, integer())
pmax(1:2, integer())

# dropped
cbind(1:2, integer())

# recycled to length of first
ifelse(rep(TRUE, 4), integer(), character())

# preserved-ish
paste(1:2, integer())

# Errors
data.frame(1:2, integer())
})