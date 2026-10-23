# r2py crawler metadata
# package: whisker
# source_type: rd_example
# topic: rowSplit.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\whisker\help
# lines: 10

suppressPackageStartupMessages(library(whisker))
dat <- head(InsectSprays)
dat <- unname(rowSplit(dat))

template <- 
"{{#dat}}
count: {{count}}, spray: {{spray}}\n
{{/dat}}"

whisker.render(template)