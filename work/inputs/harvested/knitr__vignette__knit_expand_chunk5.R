# r2py crawler metadata
# package: knitr
# source_type: vignette
# topic: knit_expand_chunk5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\doc\knit_expand.Rmd
# lines: 4

suppressPackageStartupMessages(library(knitr))
knit_expand(text = 'you cannot see the value of x {{x=rnorm(1)}}but it is indeed created: x = {{x}}')
res = knit_expand(text = c(' x | x^2', '{{x=1:5;paste(sprintf("%2d | %3d", x, x^2), collapse = "\n")}}'))
cat(res)