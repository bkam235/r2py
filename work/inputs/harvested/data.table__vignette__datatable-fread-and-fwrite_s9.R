# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-fread-and-fwrite_s9
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-fread-and-fwrite.R
# lines: 10

suppressPackageStartupMessages(library(data.table))
dt_quoting_scenario = data.table(
  text_field = c("Contains,a,comma", "Contains \"a quote\"", "Clean_text", "", NA),
  numeric_field = 1:5
)
temp_quote_adv = tempfile(fileext = ".csv")

fwrite(dt_quoting_scenario, temp_quote_adv)
# Note the output: the empty string is quoted (""), but the NA is not.
cat(readLines(temp_quote_adv), sep = "\n")