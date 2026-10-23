# r2py crawler metadata
# package: magrittr
# source_type: vignette
# topic: magrittr_s11
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\magrittr\doc\magrittr.R
# lines: 6

suppressPackageStartupMessages(library(magrittr))
rnorm(100) %>% `*`(5) %>% `+`(5) %>% 
{
  cat("Mean:", mean(.), "Variance:", var(.),  "\n")
  head(.)
}