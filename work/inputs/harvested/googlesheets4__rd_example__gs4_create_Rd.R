# r2py crawler metadata
# package: googlesheets4
# source_type: rd_example
# topic: gs4_create.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googlesheets4\help
# lines: 32

suppressPackageStartupMessages(library(googlesheets4))
if (gs4_has_token()) withAutoprint({ # examplesIf
gs4_create("gs4-create-demo-1")

gs4_create("gs4-create-demo-2", locale = "en_CA")

gs4_create(
  "gs4-create-demo-3",
  locale = "fr_FR",
  timeZone = "Europe/Paris"
)

gs4_create(
  "gs4-create-demo-4",
  sheets = c("alpha", "beta")
)

my_data <- data.frame(x = 1)
gs4_create(
  "gs4-create-demo-5",
  sheets = my_data
)

gs4_create(
  "gs4-create-demo-6",
  sheets = list(chickwts = head(chickwts), mtcars = head(mtcars))
)

# Clean up
gs4_find("gs4-create-demo") %>%
  googledrive::drive_trash()
}) # examplesIf