# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: tstrsplit.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 35

suppressPackageStartupMessages(library(data.table))
x = c("abcde", "ghij", "klmnopq")
strsplit(x, "", fixed=TRUE)
tstrsplit(x, "", fixed=TRUE)
tstrsplit(x, "", fixed=TRUE, fill="<NA>")

# using keep to return just 1,3,5
tstrsplit(x, "", fixed=TRUE, keep=c(1,3,5))

# names argument
tstrsplit(x, "", fixed=TRUE, keep=c(1,3,5), names=LETTERS[1:3])

DT = data.table(x=c("A/B", "A", "B"), y=1:3)
DT[, c("c1") := tstrsplit(x, "/", fixed=TRUE, keep=1L)][]
DT[, c("c1", "c2") := tstrsplit(x, "/", fixed=TRUE)][]

# type.convert argument
DT = data.table(
  w = c("Yes/F", "No/M"),
  x = c("Yes 2000-03-01 A/T", "No 2000-04-01 E/R"),
  y = c("1/1/2", "2/5/2.5"),
  z = c("Yes/1/2", "No/5/3.5"),
  v = c("Yes 10 30.5 2000-03-01 A/T", "No 20 10.2 2000-04-01 E/R"))

# convert each element in the transpose list to type factor
DT[, tstrsplit(w, "/", type.convert=as.factor)]

# convert part and leave any others
DT[, tstrsplit(z, "/", type.convert=list(as.numeric=2:3))]

# convert part with one function and any others with another
DT[, tstrsplit(z, "/", type.convert=list(as.factor=1L, as.numeric))]

# convert the remaining using 'type.convert(x, as.is=TRUE)' (i.e. what type.convert=TRUE does)
DT[, tstrsplit(v, " ", type.convert=list(as.IDate=4L, function(x) type.convert(x, as.is=TRUE)))]