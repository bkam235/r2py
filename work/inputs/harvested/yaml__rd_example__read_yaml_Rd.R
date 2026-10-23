# r2py crawler metadata
# package: yaml
# source_type: rd_example
# topic: read_yaml.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\yaml\help
# lines: 14

suppressPackageStartupMessages(library(yaml))
# reading from a file connection
  filename <- tempfile()
  cat("test: data\n", file = filename)
  con <- file(filename, "r")
  read_yaml(con)
  close(con)

  # using a filename to specify input file
  read_yaml(filename)


  # reading from a character vector
  read_yaml(text="- hey\n- hi\n- hello")