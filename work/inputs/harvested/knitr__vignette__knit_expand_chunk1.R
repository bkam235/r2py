# r2py crawler metadata
# package: knitr
# source_type: vignette
# topic: knit_expand_chunk1
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\doc\knit_expand.Rmd
# lines: 4

library(knitr)
knit_expand(text = 'The value of pi is {{pi}}.')
knit_expand(text = 'The value of a is {{a}}, so a + 1 is {{a+1}}.', a = rnorm(1))
knit_expand(text = 'The area of a circle with radius {{r}} is {{pi*r^2}}', r = 5)