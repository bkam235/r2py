# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: setkey.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 40

suppressPackageStartupMessages(library(data.table))
# Type 'example(setkey)' to run these at the prompt and browse output

DT = data.table(A=5:1,B=letters[5:1])
DT # before
setkey(DT,B)          # re-orders table and marks it sorted.
DT # after
tables()              # KEY column reports the key'd columns
key(DT)
keycols = c("A","B")
setkeyv(DT,keycols)

DT = data.table(A=5:1,B=letters[5:1])
DT2 = DT              # does not copy
setkey(DT2,B)         # does not copy-on-write to DT2
identical(DT,DT2)     # TRUE. DT and DT2 are two names for the same keyed table

DT = data.table(A=5:1,B=letters[5:1])
DT2 = copy(DT)        # explicit copy() needed to copy a data.table
setkey(DT2,B)         # now just changes DT2
identical(DT,DT2)     # FALSE. DT and DT2 are now different tables

DT = data.table(A=5:1,B=letters[5:1])
setindex(DT)          # set indices
setindex(DT, A)
setindex(DT, B)
indices(DT)           # get indices single vector
indices(DT, vectors = TRUE) # get indices list

# Setting multiple indices at once
DT = data.table(A = 5:1, B = letters[5:1], C = 10:6)
setindexv(DT, list(c("A", "B"), c("B", "C")))
print(DT, show.indices=TRUE)

# Use the dot .(subset_value) syntax with integer keys:
DT = data.table(id = 2:1)
setkey(DT, id)
subset_value <- 1
DT[subset_value]  # treats subset_value as an row number
DT[.(subset_value)]  # matches subset_value against key column (id)