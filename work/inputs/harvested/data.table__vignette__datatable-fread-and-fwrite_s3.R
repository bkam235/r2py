# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-fread-and-fwrite_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-fread-and-fwrite.R
# lines: 13

# Create a sample file with some unwanted lines
writeLines(
'HEADER: Some metadata
HEADER: More metadata
1 2.0 3.0
2 4.5 6.7
HEADER: Yet more
3 8.9 0.1
4 1.2 3.4',
"example_data.txt")

library(data.table)
fread("grep -v HEADER example_data.txt")