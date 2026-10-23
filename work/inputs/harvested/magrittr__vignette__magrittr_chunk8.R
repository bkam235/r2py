# r2py crawler metadata
# package: magrittr
# source_type: vignette
# topic: magrittr_chunk8
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\magrittr\doc\magrittr.Rmd
# lines: 7

suppressPackageStartupMessages(library(magrittr))
iris %>%
  subset(Sepal.Length > mean(Sepal.Length)) %$%
  cor(Sepal.Length, Sepal.Width)
   
data.frame(z = rnorm(100)) %$% 
  ts.plot(z)