# r2py crawler metadata
# package: plyr
# source_type: rd_example
# topic: progress_tk.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\plyr\help
# lines: 4

suppressPackageStartupMessages(library(plyr))
l_ply(1:100, identity, .progress = "tk")
l_ply(1:100, identity, .progress = progress_tk(width=400))
l_ply(1:100, identity, .progress = progress_tk(label=""))