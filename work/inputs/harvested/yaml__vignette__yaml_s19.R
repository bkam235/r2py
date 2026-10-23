# r2py crawler metadata
# package: yaml
# source_type: vignette
# topic: yaml_s19
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\yaml\doc\yaml.R
# lines: 4

suppressPackageStartupMessages(library(yaml))
result <- c("true", "false")
class(result) <- "verbatim"
cat(as.yaml(result))