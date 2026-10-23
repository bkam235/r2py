# r2py crawler metadata
# package: magrittr
# source_type: rd_example
# topic: exposition.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\magrittr\help
# lines: 7

suppressPackageStartupMessages(library(magrittr))
iris %>%
  subset(Sepal.Length > mean(Sepal.Length)) %$%
  cor(Sepal.Length, Sepal.Width)
  
data.frame(z = rnorm(100)) %$% 
  ts.plot(z)