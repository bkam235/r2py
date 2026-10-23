# r2py crawler metadata
# package: readxl
# source_type: rd_example
# topic: excel_sheets.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readxl\help
# lines: 7

suppressPackageStartupMessages(library(readxl))
excel_sheets(readxl_example("datasets.xlsx"))
excel_sheets(readxl_example("datasets.xls"))

# To load all sheets in a workbook, use lapply()
path <- readxl_example("datasets.xls")
lapply(excel_sheets(path), read_excel, path = path)