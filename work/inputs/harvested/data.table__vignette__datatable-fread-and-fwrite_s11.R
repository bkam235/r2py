# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-fread-and-fwrite_s11
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-fread-and-fwrite.R
# lines: 8

suppressPackageStartupMessages(library(data.table))
if (requireNamespace("bit64", quietly = TRUE)) {
  dt_i64 = data.table(uid = bit64::as.integer64("1234567890123456789"), val = 100)
  temp_i64_out = tempfile(fileext = ".csv")
  fwrite(dt_i64, temp_i64_out)
  cat(readLines(temp_i64_out), sep = "\n")
  unlink(temp_i64_out)
}