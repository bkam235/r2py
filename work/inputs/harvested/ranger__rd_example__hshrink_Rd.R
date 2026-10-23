# r2py crawler metadata
# package: ranger
# source_type: rd_example
# topic: hshrink.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ranger\help
# lines: 4

suppressPackageStartupMessages(library(ranger))
## Hierarchical shrinkage for a probablity forest
rf <- ranger(Species ~ ., iris, node.stats = TRUE, probability = TRUE)
hshrink(rf, lambda = 5)