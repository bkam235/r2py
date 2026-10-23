# r2py crawler metadata
# package: mlbench
# source_type: rd_example
# topic: Zoo.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\mlbench\help
# lines: 9

suppressPackageStartupMessages(library(mlbench))
data("Zoo", package = "mlbench")
summary(Zoo)

## see the annimals grouped by type
split(rownames(Zoo), Zoo$type)

## which animals have fins?
rownames(Zoo)[Zoo$fins]