# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: drive_share.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 32

suppressPackageStartupMessages(library(googledrive))
if (drive_has_token()) withAutoprint({ # examplesIf
# Create a file to share
file <- drive_example_remote("chicken_doc") |>
  drive_cp(name = "chicken-share.txt")

# Let a specific person comment
file <- file |>
  drive_share(
    role = "commenter",
    type = "user",
    emailAddress = "susan@example.com"
  )

# Let a different specific person edit and customize the email notification
file <- file |>
  drive_share(
    role = "writer",
    type = "user",
    emailAddress = "carol@example.com",
    emailMessage = "Would appreciate your feedback on this!"
  )

# Let anyone read the file
file <- file |>
  drive_share(role = "reader", type = "anyone")
# Single-purpose wrapper function for this
drive_share_anyone(file)

# Clean up
drive_rm(file)
}) # examplesIf