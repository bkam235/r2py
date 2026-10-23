# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: transform.data.table.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 26

suppressPackageStartupMessages(library(data.table))
DT <- data.table(a=rep(1:3, each=2), b=1:6)

DT2 <- transform(DT, c = a^2)
DT[, c:=a^2]
identical(DT,DT2)

DT2 <- within(DT, {
  b <- rev(b)
  c <- a*2
  rm(a)
})
DT[,`:=`(b = rev(b),
         c = a*2,
         a = NULL)]
identical(DT,DT2)

DT$d = ave(DT$b, DT$c, FUN=max)               # copies entire DT, even if it is 10GiB in RAM
DT = DT[, transform(.SD, d=max(b)), by="c"]   # same, but even worse as .SD is copied for each group
DT[, d:=max(b), by="c"]                       # same result, but much faster, shorter and scales

# Multiple update by group. Convenient, fast, scales and easy to read.
DT[, `:=`(minb = min(b),
          meanb = mean(b),
          bplusd = sum(b+d)),  by=c%/%5]
DT