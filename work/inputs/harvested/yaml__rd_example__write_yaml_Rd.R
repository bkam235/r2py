# r2py crawler metadata
# package: yaml
# source_type: rd_example
# topic: write_yaml.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\yaml\help
# lines: 9

suppressPackageStartupMessages(library(yaml))
# writing to a file connection
  filename <- tempfile()
  con <- file(filename, "w")
  write_yaml(data.frame(a=1:10, b=letters[1:10], c=11:20), con)
  close(con)

  # using a filename to specify output file
  write_yaml(data.frame(a=1:10, b=letters[1:10], c=11:20), filename)