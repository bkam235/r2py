# r2py crawler metadata
# package: yaml
# source_type: vignette
# topic: yaml_s21
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\yaml\doc\yaml.R
# lines: 4

suppressPackageStartupMessages(library(yaml))
x <- 1:3
attr(x, "tag") <- "!custom"
cat(as.yaml(x))