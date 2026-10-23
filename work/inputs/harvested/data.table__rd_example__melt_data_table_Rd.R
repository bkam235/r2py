# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: melt.data.table.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 74

set.seed(45)
require(data.table)
DT <- data.table(
  i_1 = c(1:5, NA),
  n_1 = c(NA, 6, 7, 8, 9, 10),
  f_1 = factor(sample(c(letters[1:3], NA), 6L, TRUE)),
  f_2 = factor(c("z", "a", "x", "c", "x", "x"), ordered=TRUE),
  c_1 = sample(c(letters[1:3], NA), 6L, TRUE),
  c_2 = sample(c(LETTERS[1:2], NA), 6L, TRUE),
  d_1 = as.Date(c(1:3,NA,4:5), origin="2013-09-01"),
  d_2 = as.Date(6:1, origin="2012-01-01")
)
# add a couple of list cols
DT[, l_1 := DT[, list(c=list(rep(i_1, sample(5, 1L)))), by = i_1]$c]
DT[, l_2 := DT[, list(c=list(rep(c_1, sample(5, 1L)))), by = i_1]$c]

# id.vars, measure.vars as character/integer/numeric vectors
melt(DT, id.vars=1:2, measure.vars="f_1")
melt(DT, id.vars=c("i_1", "n_1"), measure.vars=3) # same as above
melt(DT, id.vars=1:2, measure.vars=3L, value.factor=TRUE) # same, but 'value' is factor
melt(DT, id.vars=1:2, measure.vars=3:4, value.factor=TRUE) # 'value' is *ordered* factor

# preserves attribute when types are identical, ex: Date
melt(DT, id.vars=3:4, measure.vars=c("d_1", "d_2"))
melt(DT, id.vars=3:4, measure.vars=c("n_1", "d_1")) # attribute not preserved

# on list
melt(DT, id.vars=1, measure.vars=c("l_1", "l_2")) # value is a list
suppressWarnings(
  melt(DT, id.vars=1, measure.vars=c("c_1", "l_1")) # c1 coerced to list, with warning
)

# on character
melt(DT, id.vars=1, measure.vars=c("c_1", "f_1")) # value is char
suppressWarnings(
  melt(DT, id.vars=1, measure.vars=c("c_1", "n_1")) # n_1 coerced to char, with warning
)

# on na.rm=TRUE. NAs are removed efficiently, from within C
melt(DT, id.vars=1, measure.vars=c("c_1", "c_2"), na.rm=TRUE) # remove NA

# measure.vars can be also a list
# melt "f_1,f_2" and "d_1,d_2" simultaneously, retain 'factor' attribute
# convenient way using internal function patterns()
melt(DT, id.vars=1:2, measure.vars=patterns("^f_", "^d_"), value.factor=TRUE)
melt(DT, id.vars=patterns("[in]"), measure.vars=patterns("^f_", "^d_"), value.factor=TRUE)
# same as above, but provide list of columns directly by column names or indices
melt(DT, id.vars=1:2, measure.vars=list(3:4, c("d_1", "d_2")), value.factor=TRUE)
# same as above, but provide names directly:
melt(DT, id.vars=1:2, measure.vars=patterns(f="^f_", d="^d_"), value.factor=TRUE)

# na.rm=TRUE removes rows with NAs in any 'value' columns
melt(DT, id.vars=1:2, measure.vars=patterns("f_", "d_"), value.factor=TRUE, na.rm=TRUE)

# 'na.rm=TRUE' also works with list column, but note that is.na only
# returns TRUE if the list element is a length=1 vector with an NA.
is.na(list(one.NA=NA, two.NA=c(NA,NA)))
melt(DT, id.vars=1:2, measure.vars=patterns("l_", "d_"), na.rm=FALSE)
melt(DT, id.vars=1:2, measure.vars=patterns("l_", "d_"), na.rm=TRUE)

# measure list with missing/short entries results in output with runs of NA
DT.missing.cols <- DT[, .(d_1, d_2, c_1, f_2)]
melt(DT.missing.cols, measure.vars=list(d=1:2, c="c_1", f=c(NA, "f_2")))

# specifying columns to melt via separator.
melt(DT.missing.cols, measure.vars=measure(value.name, number=as.integer, sep="_"))

# specifying columns to melt via regex.
melt(DT.missing.cols, measure.vars=measure(value.name, number=as.integer, pattern="(.)_(.)"))
melt(DT.missing.cols, measure.vars=measure(value.name, number=as.integer, pattern="([dc])_(.)"))

# cols arg of measure can be used if you do not want to use regex
melt(DT.missing.cols, measure.vars=measure(
  value.name, number=as.integer, sep="_", cols=c("d_1","d_2","c_1")))