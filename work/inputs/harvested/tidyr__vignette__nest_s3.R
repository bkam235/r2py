# r2py crawler metadata
# package: tidyr
# source_type: vignette
# topic: nest_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\doc\nest.R
# lines: 11

suppressPackageStartupMessages(library(tidyr))
df1 <- tibble(
  g = c(1, 2, 3),
  data = list(
    tibble(x = 1, y = 2),
    tibble(x = 4:5, y = 6:7),
    tibble(x = 10)
  )
)

df1