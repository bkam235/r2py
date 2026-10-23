# r2py crawler metadata
# package: readxl
# source_type: rd_example
# topic: read_excel.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readxl\help
# lines: 69

suppressPackageStartupMessages(library(readxl))
datasets <- readxl_example("datasets.xlsx")
read_excel(datasets)

# Specify sheet either by position or by name
read_excel(datasets, 2)
read_excel(datasets, "mtcars")

# Skip rows and use default column names
read_excel(datasets, skip = 10, col_names = FALSE)

# Recycle a single column type
read_excel(datasets, col_types = "text")

# Specify some col_types and guess others
read_excel(
  readxl_example("deaths.xlsx"),
  skip = 4, n_max = 10, col_names = TRUE,
  col_types = c("text", "text", "guess", "guess", "guess", "guess")
)

# Accomodate a column with disparate types via col_type = "list"
df <- read_excel(readxl_example("clippy.xlsx"), col_types = c("text", "list"))
df
df$value
sapply(df$value, class)

# Limit the number of data rows read
read_excel(datasets, n_max = 3)

# Read from an Excel range using A1 or R1C1 notation
read_excel(datasets, range = "C1:E7")
read_excel(datasets, range = "R1C2:R2C5")

# Specify the sheet as part of the range
read_excel(datasets, range = "mtcars!B1:D5")

# Read only specific rows or columns
read_excel(datasets, range = cell_rows(102:151), col_names = FALSE)
read_excel(datasets, range = cell_cols("B:D"))

# Get a preview of column names
names(read_excel(readxl_example("datasets.xlsx"), n_max = 0))

# exploit full .name_repair flexibility from tibble

# "universal" names are unique and syntactic
read_excel(
  readxl_example("deaths.xlsx"),
  range = "arts!A5:F15",
  .name_repair = "universal"
)

# specify name repair as a built-in function
read_excel(readxl_example("clippy.xlsx"), .name_repair = toupper)

# specify name repair as a custom function
my_custom_name_repair <- function(nms) tolower(gsub("[.]", "_", nms))
read_excel(
  readxl_example("datasets.xlsx"),
  .name_repair = my_custom_name_repair
)

# specify name repair as an anonymous function
read_excel(
  readxl_example("datasets.xlsx"),
  sheet = "chickwts",
  .name_repair = ~ substr(.x, start = 1, stop = 3)
)