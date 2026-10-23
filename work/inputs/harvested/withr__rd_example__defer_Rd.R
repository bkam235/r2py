# r2py crawler metadata
# package: withr
# source_type: rd_example
# topic: defer.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\withr\help
# lines: 31

suppressPackageStartupMessages(library(withr))
# define a 'local' function that creates a file, and
# removes it when the parent function has finished executing
local_file <- function(path) {
  file.create(path)
  defer_parent(unlink(path))
}

# create tempfile path
path <- tempfile()

# use 'local_file' in a function
local({
  local_file(path)
  stopifnot(file.exists(path))
})

# file is deleted as we leave 'local' local
stopifnot(!file.exists(path))

# investigate how 'defer' modifies the
# executing function's environment
local({
  local_file(path)
  print(attributes(environment()))
})

# Note that examples lack function scoping so deferred calls are
# generally executed immediately
defer(print("one"))
defer(print("two"))