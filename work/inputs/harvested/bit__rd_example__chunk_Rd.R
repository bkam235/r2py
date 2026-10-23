# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: chunk.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 10

suppressPackageStartupMessages(library(bit))
chunk(complex(1e7))
  chunk(raw(1e7))
  chunk(raw(1e7), length=3)

  chunks(1, 10, 3)
  # no longer do
  chunk(1, 100, 10)
  # but for bckward compatibility this works
  chunk(from=1, to=100, by=10)