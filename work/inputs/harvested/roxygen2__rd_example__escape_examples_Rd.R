# r2py crawler metadata
# package: roxygen2
# source_type: rd_example
# topic: escape_examples.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\roxygen2\help
# lines: 27

suppressPackageStartupMessages(library(roxygen2))
# In examples we automatically escape Rd comments (%):
100 %% 30
# even if they are in strings
"50%"

# and \ and \v inside of strings and symbols
"\v" # vertical tab
"\\"
# but not comments: \l \v

# other string escapes are left as is
"\""
"\n"

# Otherwise, backslashes and parentheses are left as is. This
# means that you need to escape unbalanced parentheses, which typically only
# occur in \dontshow{}:
if (FALSE) { 
print("Hello")
 } 

# You also need to escape backslashes in infix operators and comments
# (this is generally rare)
`%\\%` <- function(x, y) x + y
10 %\% 20
# \\ (renders as two backslashes)