# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: resourcePaths.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 8

suppressPackageStartupMessages(library(shiny))
addResourcePath('datasets', system.file('data', package='datasets'))
resourcePaths()
removeResourcePath('datasets')
resourcePaths()

# make sure all resources are removed
lapply(names(resourcePaths()), removeResourcePath)