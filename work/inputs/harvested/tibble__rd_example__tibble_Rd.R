# r2py crawler metadata
# package: tibble
# source_type: rd_example
# topic: tibble.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tibble\help
# lines: 97

suppressPackageStartupMessages(library(tibble))
# Unnamed arguments are named with their expression:
a <- 1:5
tibble(a, a * 2)

# Scalars (vectors of length one) are recycled:
tibble(a, b = a * 2, c = 1)

# Columns are available in subsequent expressions:
tibble(x = runif(10), y = x * 2)

# tibble() never coerces its inputs,
str(tibble(letters))
str(tibble(x = list(diag(1), diag(2))))

# or munges column names (unless requested),
tibble(`a + b` = 1:5)

# but it forces you to take charge of names, if they need repair:
try(tibble(x = 1, x = 2))
tibble(x = 1, x = 2, .name_repair = "unique")
tibble(x = 1, x = 2, .name_repair = "minimal")

## By default, non-syntactic names are allowed,
df <- tibble(`a 1` = 1, `a 2` = 2)
## because you can still index by name:
df[["a 1"]]
df$`a 1`
with(df, `a 1`)

## Syntactic names are easier to work with, though, and you can request them:
df <- tibble(`a 1` = 1, `a 2` = 2, .name_repair = "universal")
df$a.1

## You can specify your own name repair function:
tibble(x = 1, x = 2, .name_repair = make.unique)

fix_names <- function(x) gsub("\\s+", "_", x)
tibble(`year 1` = 1, `year 2` = 2, .name_repair = fix_names)

## purrr-style anonymous functions and constants
## are also supported
tibble(x = 1, x = 2, .name_repair = ~ make.names(., unique = TRUE))

tibble(x = 1, x = 2, .name_repair = ~ c("a", "b"))

# Tibbles can contain columns that are tibbles or matrices
# if the number of rows is compatible. Unnamed tibbled are
# spliced, i.e. the inner columns are inserted into the
# tibble under construction.
tibble(
  a = 1:3,
  tibble(
    b = 4:6,
    c = 7:9
  ),
  d = tibble(
    e = tibble(
      f = b
    )
  )
)
tibble(
  a = 1:3,
  b = diag(3),
  c = cor(trees),
  d = Titanic[1:3, , , ]
)

# Data can not contain tibbles or matrices with incompatible number of rows:
try(tibble(a = 1:3, b = tibble(c = 4:7)))

# Use := to create columns with names that start with a dot:
tibble(.dotted := 3)

# This also works, but might break in the future:
tibble(.dotted = 3)

# You can unquote an expression:
x <- 3
tibble(x = 1, y = x)
tibble(x = 1, y = !!x)

# You can splice-unquote a list of quosures and expressions:
tibble(!!!list(x = rlang::quo(1:10), y = quote(x * 2)))

# Use .data, .env and !! to refer explicitly to columns or outside objects
a <- 1
tibble(a = 2, b = a)
tibble(a = 2, b = .data$a)
tibble(a = 2, b = .env$a)
tibble(a = 2, b = !!a)
try(tibble(a = 2, b = .env$bogus))
try(tibble(a = 2, b = !!bogus))

# Use tibble_row() to construct a one-row tibble:
tibble_row(a = 1, lm = lm(Height ~ Girth + Volume, data = trees))