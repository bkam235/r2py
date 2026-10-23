# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: arg_match.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 18

suppressPackageStartupMessages(library(rlang))
fn <- function(x = c("foo", "bar")) arg_match(x)
fn("bar")

# Throws an informative error for mismatches:
try(fn("b"))
try(fn("baz"))

# Use the bare-bones version with explicit values for speed:
arg_match0("bar", c("foo", "bar", "baz"))

# For convenience:
fn1 <- function(x = c("bar", "baz", "foo")) fn3(x)
fn2 <- function(x = c("baz", "bar", "foo")) fn3(x)
fn3 <- function(x) arg_match0(x, c("foo", "bar", "baz"))
fn1()
fn2("bar")
try(fn3("zoo"))