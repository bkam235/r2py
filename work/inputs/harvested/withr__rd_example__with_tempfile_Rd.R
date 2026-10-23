# r2py crawler metadata
# package: withr
# source_type: rd_example
# topic: with_tempfile.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\withr\help
# lines: 19

suppressPackageStartupMessages(library(withr))
# local_tempfile() is the easiest to use because it returns a path
local({
  path1 <<- local_tempfile(lines = c("x,y", "1,2"))
  readLines(path1)
})
# the file is deleted automatically
file.exists(path1)

# with_tempfile() is a bit trickier; the first argument gives the name
# of a variable that will contain the path:
with_tempfile("path2", {
  print(path2)
  write.csv(iris, path2)
  file.size(path2)
})

# Note that this variable is only available in the scope of with_tempfile
try(path2)