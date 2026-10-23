# r2py crawler metadata
# package: curl
# source_type: rd_example
# topic: file_writer.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\curl\help
# lines: 14

suppressPackageStartupMessages(library(curl))
# Doesn't open yet
tmp <- tempfile()
writer <- file_writer(tmp)

# Now it opens
writer(charToRaw("Hello!\n"))
writer(charToRaw("How are you?\n"))

# Close it!
writer(charToRaw("All done!\n"), close = TRUE)

# Check it worked
readLines(tmp)