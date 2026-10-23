# r2py crawler metadata
# package: devtools
# source_type: rd_example
# topic: source_url.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\devtools\help
# lines: 10

suppressPackageStartupMessages(library(devtools))
source_url("https://gist.github.com/hadley/6872663/raw/hi.r")

# With a hash, to make sure the remote file hasn't changed
source_url("https://gist.github.com/hadley/6872663/raw/hi.r",
  sha1 = "54f1db27e60bb7e0486d785604909b49e8fef9f9")

# With a truncated hash
source_url("https://gist.github.com/hadley/6872663/raw/hi.r",
  sha1 = "54f1db27e60")