# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-fread-and-fwrite_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-fread-and-fwrite.R
# lines: 4

suppressPackageStartupMessages(library(data.table))
my_data_string = "colA,colB,colC\n1,apple,TRUE\n2,banana,FALSE\n3,orange,TRUE"
dt_from_text = fread(text = my_data_string)
print(dt_from_text)