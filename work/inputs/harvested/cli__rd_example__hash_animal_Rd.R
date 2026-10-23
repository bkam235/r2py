# r2py crawler metadata
# package: cli
# source_type: rd_example
# topic: hash_animal.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cli\help
# lines: 8

suppressPackageStartupMessages(library(cli))
hash_animal(c("foo", "bar"))

# if you increase `n_adj`, the shorter hash is a suffix of the longer:
hash_animal("cli package", 0)$hash
hash_animal("cli package", 1)$hash
hash_animal("cli package", 2)$hash
hash_animal("cli package", 3)$hash