# r2py crawler metadata
# package: knitr
# source_type: vignette
# topic: knit_expand_chunk6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\doc\knit_expand.Rmd
# lines: 4

suppressPackageStartupMessages(library(knitr))
res = knit_expand(text = c('{{i=0;h2=function(x){i<<-i+1;sprintf("<h2>%d. %s</h2>", i, x)} }}<html>',
'{{h2("First Section")}}', '{{h2("Second Section")}}', '{{h2("Conclusion")}}', '</html>'))
cat(res)