# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: vec_proxy_compare.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 9

suppressPackageStartupMessages(library(vctrs))
# Lists are not comparable
x <- list(1:2, 1, 1:2, 3)
try(vec_compare(x, x))

# But lists are orderable by first appearance to allow for
# ordering data frames with list-cols
df <- new_data_frame(list(x = x))
vec_sort(df)