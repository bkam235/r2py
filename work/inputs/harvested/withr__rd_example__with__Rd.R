# r2py crawler metadata
# package: withr
# source_type: rd_example
# topic: with_.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\withr\help
# lines: 15

suppressPackageStartupMessages(library(withr))
with_(setwd)

global_stack <- list()
set_global_state <- function(state, msg = "Changing global state.") {
  global_stack <- c(list(state), global_stack)
  message(msg)
  state
}
reset_global_state <- function(state) {
  old_state <- global_stack[[1]]
  global_stack <- global_stack[-1]
  stopifnot(identical(state, old_state))
}
with_(set_global_state, reset_global_state)