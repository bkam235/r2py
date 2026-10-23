# r2py crawler metadata
# package: evaluate
# source_type: rd_example
# topic: inject_funs.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\evaluate\help
# lines: 13

library(evaluate)
# normally you cannot capture the output of system
evaluate("system('R --version')")

# replace the system() function
old <- inject_funs(system = function(...) {
  cat(base::system(..., intern = TRUE), sep = "\n")
})

evaluate("system('R --version')")

# restore previously injected functions
inject_funs(old)