# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: call_modify.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 58

suppressPackageStartupMessages(library(rlang))
call <- quote(mean(x, na.rm = TRUE))

# Modify an existing argument
call_modify(call, na.rm = FALSE)
call_modify(call, x = quote(y))

# Remove an argument
call_modify(call, na.rm = zap())

# Add a new argument
call_modify(call, trim = 0.1)

# Add an explicit missing argument:
call_modify(call, na.rm = )

# Supply a list of new arguments with `!!!`
newargs <- list(na.rm = zap(), trim = 0.1)
call <- call_modify(call, !!!newargs)
call

# Remove multiple arguments by splicing zaps:
newargs <- rep_named(c("na.rm", "trim"), list(zap()))
call <- call_modify(call, !!!newargs)
call


# Modify the `...` arguments as if it were a named argument:
call <- call_modify(call, ... = )
call

call <- call_modify(call, ... = zap())
call


# When you're working with a user-supplied call, standardise it
# beforehand in case it includes unmatched arguments:
user_call <- quote(matrix(x, nc = 3))
call_modify(user_call, ncol = 1)

# `call_match()` applies R's argument matching rules. Matching
# ensures you're modifying the intended argument.
user_call <- call_match(user_call, matrix)
user_call
call_modify(user_call, ncol = 1)


# By default, arguments with the same name are kept. This has
# subtle implications, for instance you can move an argument to
# last position by removing it and remapping it:
call <- quote(foo(bar = , baz))
call_modify(call, bar = zap(), bar = missing_arg())

# You can also choose to keep only the first or last homonym
# arguments:
args <-  list(bar = zap(), bar = missing_arg())
call_modify(call, !!!args, .homonyms = "first")
call_modify(call, !!!args, .homonyms = "last")