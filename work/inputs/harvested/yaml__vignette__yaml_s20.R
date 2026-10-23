# r2py crawler metadata
# package: yaml
# source_type: vignette
# topic: yaml_s20
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\yaml\doc\yaml.R
# lines: 4

suppressPackageStartupMessages(library(yaml))
port <- "80:80"
attr(port, "quoted") <- TRUE
cat(as.yaml(list(ports = list(port))))