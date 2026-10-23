# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: drive_get.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 56

suppressPackageStartupMessages(library(googledrive))
if (drive_has_token()) withAutoprint({ # examplesIf
# get info about your "My Drive" root folder
drive_get("~/")
# the API reserves the file id "root" for your root folder
drive_get(id = "root")
drive_get(id = "root") |> drive_reveal("path")

# set up some files to get by path
alfalfa <- drive_mkdir("alfalfa")
broccoli <- drive_upload(
  drive_example_local("chicken.txt"),
  name = "broccoli", path = alfalfa
)
drive_get("broccoli")
drive_get("alfalfa/broccoli")
drive_get("~/alfalfa/broccoli")
drive_get(c("broccoli", "alfalfa/", "~/alfalfa/broccoli"))

# Clean up
drive_rm(alfalfa)


# The examples below are indicative of correct syntax.
# But note these will generally result in an error or a
# 0-row dribble, unless you replace the inputs with paths
# or file ids that exist in your Drive.

# multiple names
drive_get(c("abc", "def"))

# multiple names, one of which must be a folder
drive_get(c("abc", "def/"))

# query by file id(s)
drive_get(id = "abcdefgeh123456789")
drive_get(as_id("abcdefgeh123456789"))
drive_get(id = c("abcdefgh123456789", "jklmnopq123456789"))

# apply to a browser URL for, e.g., a Google Sheet
my_url <- "https://docs.google.com/spreadsheets/d/FILE_ID/edit#gid=SHEET_ID"
drive_get(my_url)
drive_get(as_id(my_url))
drive_get(id = my_url)

# access the shared drive named "foo"
# shared_drive params must be specified if getting by path
foo <- shared_drive_get("foo")
drive_get(c("this.jpg", "that-file"), shared_drive = foo)
# shared_drive params are not necessary if getting by id
drive_get(as_id("123456789"))

# search all shared drives and other files user has accessed
drive_get(c("this.jpg", "that-file"), corpus = "allDrives")

}) # examplesIf