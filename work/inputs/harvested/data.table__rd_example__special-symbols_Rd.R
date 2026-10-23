# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: special-symbols.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 33

suppressPackageStartupMessages(library(data.table))
DT = data.table(x=rep(c("b","a","c"),each=3), v=c(1,1,1,2,2,1,1,2,2), y=c(1,3,6), a=1:9, b=9:1)
DT
X = data.table(x=c("c","b"), v=8:7, foo=c(4,2))
X

DT[.N]                                 # last row, only special symbol allowed in 'i'
DT[, .N]                               # total number of rows in DT
DT[, .N, by=x]                         # number of rows in each group
DT[, .SD, .SDcols=x:y]                 # select columns 'x' through 'y'
DT[, .SD[1]]                           # first row of all columns
DT[, .SD[1], by=x]                     # first row of all columns for each group in 'x'
DT[, c(.N, lapply(.SD, sum)), by=x]    # get rows *and* sum all columns by group
DT[, .I[1], by=x]                      # row number in DT corresponding to each group
DT[, .N, by=rleid(v)]                  # get count of consecutive runs of 'v'
DT[, c(.(y=max(y)), lapply(.SD, min)),
        by=rleid(v), .SDcols=v:b]      # compute 'j' for each consecutive runs of 'v'
DT[, grp := .GRP, by=x]                # add a group counter
DT[, grp_pct := .GRP/.NGRP, by=x]      # add a group "progress" counter
X[, DT[.BY, y, on="x"], by=x]          # join within each group
DT[X, on=.NATURAL]                     # join X and DT on common column similar to X[on=Y]

# .N can be different in i and j
DT[{cat(sprintf('in i, .N is %d\n', .N)); a < .N/2},
   {cat(sprintf('in j, .N is %d\n', .N)); mean(a)}]

# .I can be different in j and by, enabling rowwise operations in by
DT[, .(.I, min(.SD[,-1]))]
DT[, .(min(.SD[,-1])), by=.I]

# Do not expect this to correctly append the value of .BY in each group; copy(.BY) will work.
by_tracker = list()
DT[, { append(by_tracker, .BY); sum(v) }, by=x]