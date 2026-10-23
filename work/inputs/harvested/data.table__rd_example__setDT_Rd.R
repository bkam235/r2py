# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: setDT.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 35

suppressPackageStartupMessages(library(data.table))
set.seed(45L)
X = data.frame(
  A=sample(3, 10, TRUE),
  B=sample(letters[1:3], 10, TRUE),
  C=sample(10))

# Convert X to data.table by reference and
# get the frequency of each "A,B" combination
setDT(X)[, .N, by=.(A,B)]

# convert list to data.table
# autofill names
X = list(1:4, letters[1:4])
setDT(X)
# don't provide names
X = list(a=1:4, letters[1:4])
setDT(X, FALSE)

# setkey directly
X = list(a = 4:1, b=runif(4))
setDT(X, key="a")[]

# check.names argument
X = list(a=1:5, a=6:10)
setDT(X, check.names=TRUE)[]

# Example demonstrating setDT after loading from RDS
rds_file = tempfile(fileext = ".rds")
X = data.table(a = 1:5, b = letters[1:5])
saveRDS(X, rds_file)
X_loaded = readRDS(rds_file)
setDT(X_loaded)  # restore internal data.table attributes
print(X_loaded)
unlink(rds_file)