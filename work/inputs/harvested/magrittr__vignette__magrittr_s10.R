# r2py crawler metadata
# package: magrittr
# source_type: vignette
# topic: magrittr_s10
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\magrittr\doc\magrittr.R
# lines: 9

suppressPackageStartupMessages(library(magrittr))
rnorm(1000)    %>%
multiply_by(5) %>%
add(5)         %>%
{ 
   cat("Mean:", mean(.), 
       "Variance:", var(.), "\n")
   head(.)
}