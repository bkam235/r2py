# r2py crawler metadata
# package: tibble
# source_type: rd_example
# topic: rownames.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tibble\help
# lines: 15

suppressPackageStartupMessages(library(tibble))
# Detect row names ----------------------------------------------------
has_rownames(mtcars)
has_rownames(trees)

# Remove row names ----------------------------------------------------
remove_rownames(mtcars) %>% has_rownames()

# Convert between row names and column --------------------------------
mtcars_tbl <- rownames_to_column(mtcars, var = "car") %>% as_tibble()
mtcars_tbl
column_to_rownames(mtcars_tbl, var = "car") %>% head()

# Adding rowid as a column --------------------------------------------
rowid_to_column(trees) %>% head()