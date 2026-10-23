# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-fread-and-fwrite_s10
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-fread-and-fwrite.R
# lines: 9

suppressPackageStartupMessages(library(data.table))
dt_timestamps = data.table(
  ts = as.POSIXct("2023-10-26 14:35:45.123456", tz = "GMT"),
  dt = as.Date("2023-11-15")
)
temp_dt_iso = tempfile(fileext = ".csv")
fwrite(dt_timestamps, temp_dt_iso, dateTimeAs = "ISO")
cat(readLines(temp_dt_iso), sep = "\n")
unlink(temp_dt_iso)