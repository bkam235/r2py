# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: list_c.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 13

suppressPackageStartupMessages(library(purrr))
x1 <- list(a = 1, b = 2, c = 3)
list_c(x1)

x2 <- list(
  a = data.frame(x = 1:2),
  b = data.frame(y = "a")
)
list_rbind(x2)
list_rbind(x2, names_to = "id")
list_rbind(unname(x2), names_to = "id")

list_cbind(x2)