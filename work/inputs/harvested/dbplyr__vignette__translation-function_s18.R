# r2py crawler metadata
# package: dbplyr
# source_type: vignette
# topic: translation-function_s18
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dbplyr\doc\translation-function.R
# lines: 5

suppressPackageStartupMessages(library(dbplyr))
try({
options(dplyr.strict_sql = TRUE)
translate_sql(glob(x, y), con = con)
})