# r2py crawler metadata
# package: diffobj
# source_type: rd_example
# topic: ses.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\diffobj\help
# lines: 23

suppressPackageStartupMessages(library(diffobj))
a <- letters[1:6]
b <- c('b', 'CC', 'DD', 'd', 'f')
ses(a, b)
(dat <- ses_dat(a, b))
str(dat)                 # data.frame with a print method

## use `ses_dat` output to construct a minimal diff
## color with ANSI CSI SGR
diff <- dat[['val']]
del <- dat[['op']] == 'Delete'
ins <- dat[['op']] == 'Insert'
if(any(del))
  diff[del] <- paste0("\033[33m- ", diff[del], "\033[m")
if(any(ins))
  diff[ins] <- paste0("\033[34m+ ", diff[ins], "\033[m")
if(any(!ins & !del))
  diff[!ins & !del] <- paste0("  ", diff[!ins & !del])
writeLines(diff)

## We can recover `a` and `b` from the data
identical(subset(dat, op != 'Insert', val)[[1]], a)
identical(subset(dat, op != 'Delete', val)[[1]], b)