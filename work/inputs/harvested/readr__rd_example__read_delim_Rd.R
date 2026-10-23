# r2py crawler metadata
# package: readr
# source_type: rd_example
# topic: read_delim.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readr\help
# lines: 75

suppressPackageStartupMessages(library(readr))
# Input sources -------------------------------------------------------------
# Read from a path
read_csv(readr_example("mtcars.csv"))
read_csv(readr_example("mtcars.csv.zip"))
read_csv(readr_example("mtcars.csv.bz2"))

# Including remote paths
read_csv("https://github.com/tidyverse/readr/raw/main/inst/extdata/mtcars.csv")


# Read from multiple file paths at once
continents <- c("africa", "americas", "asia", "europe", "oceania")
filepaths <- vapply(
  paste0("mini-gapminder-", continents, ".csv"),
  FUN = readr_example,
  FUN.VALUE = character(1)
)
read_csv(filepaths, id = "file")

# Or directly from a string with `I()`
read_csv(I("x,y\n1,2\n3,4"))

# Column selection-----------------------------------------------------------
# Pass column names or indexes directly to select them
read_csv(readr_example("chickens.csv"), col_select = c(chicken, eggs_laid))
read_csv(readr_example("chickens.csv"), col_select = c(1, 3:4))

# Or use the selection helpers
read_csv(
  readr_example("chickens.csv"),
  col_select = c(starts_with("c"), last_col())
)

# You can also rename specific columns
read_csv(
  readr_example("chickens.csv"),
  col_select = c(egg_yield = eggs_laid, everything())
)

# Column types --------------------------------------------------------------
# By default, readr guesses the columns types, looking at `guess_max` rows.
# You can override with a compact specification:
read_csv(I("x,y\n1,2\n3,4"), col_types = "dc")

# Or with a list of column types:
read_csv(I("x,y\n1,2\n3,4"), col_types = list(col_double(), col_character()))

# If there are parsing problems, you get a warning, and can extract
# more details with problems()
y <- read_csv(I("x\n1\n2\nb"), col_types = list(col_double()))
y
problems(y)

# Column names --------------------------------------------------------------
# By default, readr duplicate name repair is noisy
read_csv(I("x,x\n1,2\n3,4"))

# Same default repair strategy, but quiet
read_csv(I("x,x\n1,2\n3,4"), name_repair = "unique_quiet")

# There's also a global option that controls verbosity of name repair
withr::with_options(
  list(rlib_name_repair_verbosity = "quiet"),
  read_csv(I("x,x\n1,2\n3,4"))
)

# Or use "minimal" to turn off name repair
read_csv(I("x,x\n1,2\n3,4"), name_repair = "minimal")

# File types ----------------------------------------------------------------
read_csv(I("a,b\n1.0,2.0"))
read_csv2(I("a;b\n1,0;2,0"))
read_tsv(I("a\tb\n1.0\t2.0"))
read_delim(I("a|b\n1.0|2.0"), delim = "|")