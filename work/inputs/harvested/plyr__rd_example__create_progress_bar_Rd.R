# r2py crawler metadata
# package: plyr
# source_type: rd_example
# topic: create_progress_bar.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\plyr\help
# lines: 11

suppressPackageStartupMessages(library(plyr))
# No progress bar
l_ply(1:100, identity, .progress = "none")

# Use the Tcl/Tk interface
l_ply(1:100, identity, .progress = "tk")

# Text-based progress (|======|)
l_ply(1:100, identity, .progress = "text")
# Choose a progress character, run a length of time you can see
l_ply(1:10000, identity, .progress = progress_text(char = "."))