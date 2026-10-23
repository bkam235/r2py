# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: programming_s9
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\programming.R
# lines: 6

suppressPackageStartupMessages(library(dplyr))
my_df <- function(x) {
  tibble("{{x}}_2" := x * 2)
}
my_var <- 10
my_df(my_var)