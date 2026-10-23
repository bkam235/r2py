# r2py crawler metadata
# package: readxl
# source_type: vignette
# topic: cell-and-column-types_s13
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readxl\doc\cell-and-column-types.R
# lines: 4

suppressPackageStartupMessages(library(readxl))
df <- read_excel(readxl_example("type-me.xlsx"), sheet = "date_coercion",
                 col_types = c("date", "text"))
print(df, n = Inf)