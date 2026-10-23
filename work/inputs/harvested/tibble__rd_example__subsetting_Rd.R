# r2py crawler metadata
# package: tibble
# source_type: rd_example
# topic: subsetting.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tibble\help
# lines: 42

suppressPackageStartupMessages(library(tibble))
df <- data.frame(a = 1:3, bc = 4:6)
tbl <- tibble(a = 1:3, bc = 4:6)

# Subsetting single columns:
df[, "a"]
tbl[, "a"]
tbl[, "a", drop = TRUE]
as.data.frame(tbl)[, "a"]

# Subsetting single rows with the drop argument:
df[1, , drop = TRUE]
tbl[1, , drop = TRUE]
as.list(tbl[1, ])

if ((Sys.getenv("NOT_CRAN") != "true" || Sys.getenv("IN_PKGDOWN") == "true")) withAutoprint({ # examplesIf
# Accessing non-existent columns:
df$b
tbl$b

df[["b", exact = FALSE]]
tbl[["b", exact = FALSE]]

df$bd <- c("n", "e", "w")
tbl$bd <- c("n", "e", "w")
df$b
tbl$b
}) # examplesIf

df$b <- 7:9
tbl$b <- 7:9
df$b
tbl$b

# Identical behavior:
tbl[1, ]
tbl[1, c("bc", "a")]
tbl[, c("bc", "a")]
tbl[c("bc", "a")]
tbl["a"]
tbl$a
tbl[["a"]]