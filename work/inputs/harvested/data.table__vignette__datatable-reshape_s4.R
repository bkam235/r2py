# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-reshape_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-reshape.R
# lines: 12

suppressPackageStartupMessages(library(data.table))
s1 <- "family_id age_mother dob_child1 dob_child2 dob_child3
1         30 1998-11-26 2000-01-29         NA
2         27 1996-06-22         NA         NA
3         26 2002-07-11 2004-04-05 2007-09-02
4         32 2004-10-10 2009-08-27 2012-07-21
5         29 2000-12-05 2005-02-28         NA"
DT <- fread(s1)
DT
## dob stands for date of birth.

str(DT)