# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: explain.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 20

suppressPackageStartupMessages(library(dplyr))
if (requireNamespace("dbplyr", quietly = TRUE) && requireNamespace("RSQLite", quietly = TRUE)) withAutoprint({ # examplesIf

lahman_s <- dbplyr::lahman_sqlite()
batting <- tbl(lahman_s, "Batting")
batting |> show_query()
batting |> explain()

# The batting database has indices on all ID variables:
# SQLite automatically picks the most restrictive index
batting |> filter(lgID == "NL" & yearID == 2000L) |> explain()

# OR's will use multiple indexes
batting |> filter(lgID == "NL" | yearID == 2000) |> explain()

# Joins will use indexes in both tables
teams <- tbl(lahman_s, "Teams")
batting |> left_join(teams, c("yearID", "teamID")) |> explain()

}) # examplesIf