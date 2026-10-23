# r2py crawler metadata
# package: vroom
# source_type: rd_example
# topic: vroom_fwf.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vroom\help
# lines: 15

suppressPackageStartupMessages(library(vroom))
fwf_sample <- vroom_example("fwf-sample.txt")
writeLines(vroom_lines(fwf_sample))

# You can specify column positions in several ways:
# 1. Guess based on position of empty columns
vroom_fwf(fwf_sample, fwf_empty(fwf_sample, col_names = c("first", "last", "state", "ssn")))
# 2. A vector of field widths
vroom_fwf(fwf_sample, fwf_widths(c(20, 10, 12), c("name", "state", "ssn")))
# 3. Paired vectors of start and end positions
vroom_fwf(fwf_sample, fwf_positions(c(1, 30), c(20, 42), c("name", "ssn")))
# 4. Named arguments with start and end positions
vroom_fwf(fwf_sample, fwf_cols(name = c(1, 20), ssn = c(30, 42)))
# 5. Named arguments with column widths
vroom_fwf(fwf_sample, fwf_cols(name = 20, state = 10, ssn = 12))