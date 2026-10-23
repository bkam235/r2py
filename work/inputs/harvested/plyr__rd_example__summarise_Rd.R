# r2py crawler metadata
# package: plyr
# source_type: rd_example
# topic: summarise.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\plyr\help
# lines: 10

suppressPackageStartupMessages(library(plyr))
# Let's extract the number of teams and total period of time
# covered by the baseball dataframe
summarise(baseball,
 duration = max(year) - min(year),
 nteams = length(unique(team)))
# Combine with ddply to do that for each separate id
ddply(baseball, "id", summarise,
 duration = max(year) - min(year),
 nteams = length(unique(team)))