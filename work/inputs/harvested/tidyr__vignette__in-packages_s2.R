# r2py crawler metadata
# package: tidyr
# source_type: vignette
# topic: in-packages_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\doc\in-packages.R
# lines: 8

library(tidyr)
library(dplyr, warn.conflicts = FALSE)
library(purrr)

packageVersion("tidyr")

mini_iris <- as_tibble(iris)[c(1, 2, 51, 52, 101, 102), ]
mini_iris