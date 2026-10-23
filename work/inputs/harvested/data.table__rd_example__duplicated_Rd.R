# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: duplicated.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 49

suppressPackageStartupMessages(library(data.table))
DT <- data.table(A = rep(1:3, each=4), B = rep(1:4, each=3),
                  C = rep(1:2, 6), key = c("A", "B"))
duplicated(DT)
unique(DT)

duplicated(DT, by="B")
unique(DT, by="B")

duplicated(DT, by=c("A", "C"))
unique(DT, by=c("A", "C"))

DT = data.table(a=c(2L,1L,2L), b=c(1L,2L,1L))   # no key
unique(DT)                   # rows 1 and 2 (row 3 is a duplicate of row 1)

DT = data.table(a=c(3.142, 4.2, 4.2, 3.142, 1.223, 1.223), b=rep(1,6))
unique(DT)                   # rows 1,2 and 5

DT = data.table(a=tan(pi*(1/4 + 1:10)), b=rep(1,10))   # example from ?all.equal
length(unique(DT$a))         # 10 strictly unique floating point values
all.equal(DT$a,rep(1,10))    # TRUE, all within tolerance of 1.0
DT[,which.min(a)]            # row 10, the strictly smallest floating point value
identical(unique(DT),DT[1])  # TRUE, stable within tolerance
identical(unique(DT),DT[10]) # FALSE

# fromLast = TRUE vs. FALSE
DT <- data.table(A = c(1, 1, 2, 2, 3), B = c(1, 2, 1, 1, 2), C = c("a", "b", "a", "b", "a"))

duplicated(DT, by="B", fromLast=FALSE) # rows 3,4,5 are duplicates
unique(DT, by="B", fromLast=FALSE) # equivalent: DT[!duplicated(DT, by="B", fromLast=FALSE)]

duplicated(DT, by="B", fromLast=TRUE) # rows 1,2,3 are duplicates
unique(DT, by="B", fromLast=TRUE) # equivalent: DT[!duplicated(DT, by="B", fromLast=TRUE)]

# anyDuplicated
anyDuplicated(DT, by=c("A", "B"))    # 3L
any(duplicated(DT, by=c("A", "B")))  # TRUE

# uniqueN, unique rows on key columns
uniqueN(DT, by = key(DT))
# uniqueN, unique rows on all columns
uniqueN(DT)
# uniqueN while grouped by "A"
DT[, .(uN=uniqueN(.SD)), by=A]

# uniqueN's na.rm=TRUE
x = sample(c(NA, NaN, runif(3)), 10, TRUE)
uniqueN(x, na.rm = FALSE) # 5, default
uniqueN(x, na.rm=TRUE) # 3