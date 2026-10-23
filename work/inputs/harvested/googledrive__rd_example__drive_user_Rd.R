# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: drive_user.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 8

suppressPackageStartupMessages(library(googledrive))
if (drive_has_token()) withAutoprint({ # examplesIf
drive_user()

# more info is returned than is printed
user <- drive_user()
str(user)
}) # examplesIf