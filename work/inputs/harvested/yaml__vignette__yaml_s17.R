# r2py crawler metadata
# package: yaml
# source_type: vignette
# topic: yaml_s17
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\yaml\doc\yaml.R
# lines: 5

suppressPackageStartupMessages(library(yaml))
cat(as.yaml(
  Sys.Date(),
  handlers = list(Date = function(x) format(x, "%Y/%m/%d"))
))