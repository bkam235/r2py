# r2py crawler metadata
# package: plyr
# source_type: rd_example
# topic: match_df.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\plyr\help
# lines: 12

suppressPackageStartupMessages(library(plyr))
# count the occurrences of each id in the baseball dataframe, then get the subset with a freq >25
longterm <- subset(count(baseball, "id"), freq > 25)
# longterm
#             id freq
# 30   ansonca01   27
# 48   baineha01   27
# ...
# Select only rows from these longterm players from the baseball dataframe
# (match would default to match on shared column names, but here was explicitly set "id")
bb_longterm <- match_df(baseball, longterm, on="id")
bb_longterm[1:5,]