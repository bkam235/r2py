# r2py crawler metadata
# package: tidyr
# source_type: vignette
# topic: programming_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\doc\programming.R
# lines: 4

library(tidyr)

iris |>
  nest(data = !Species)