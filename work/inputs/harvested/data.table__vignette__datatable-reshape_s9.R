# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-reshape_s9
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-reshape.R
# lines: 10

suppressPackageStartupMessages(library(data.table))
s2 <- "family_id age_mother name_child1 name_child2 name_child3 gender_child1 gender_child2 gender_child3
1         30         Ben        Anna          NA             1             2            NA
2         27         Tom          NA          NA             2            NA            NA
3         26         Lia         Sam         Amy             2             2             1
4         32         Max         Zoe         Joe             1             1             1
5         29         Dan         Eva          NA             2             1            NA"
DT <- fread(s2)
DT
## 1 = female, 2 = male