# r2py crawler metadata
# package: cli
# source_type: rd_example
# topic: pluralize.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cli\help
# lines: 35

suppressPackageStartupMessages(library(cli))
if (requireNamespace("glue", quietly = TRUE)) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
# Regular plurals
nfile <- 0; pluralize("Found {nfile} file{?s}.")
nfile <- 1; pluralize("Found {nfile} file{?s}.")
nfile <- 2; pluralize("Found {nfile} file{?s}.")

# Irregular plurals
ndir <- 1; pluralize("Found {ndir} director{?y/ies}.")
ndir <- 5; pluralize("Found {ndir} director{?y/ies}.")

# Use 'no' instead of zero
nfile <- 0; pluralize("Found {no(nfile)} file{?s}.")
nfile <- 1; pluralize("Found {no(nfile)} file{?s}.")
nfile <- 2; pluralize("Found {no(nfile)} file{?s}.")

# Use the length of character vectors
pkgs <- "pkg1"
pluralize("Will remove the {pkgs} package{?s}.")
pkgs <- c("pkg1", "pkg2", "pkg3")
pluralize("Will remove the {pkgs} package{?s}.")

pkgs <- character()
pluralize("Will remove {?no/the/the} {pkgs} package{?s}.")
pkgs <- c("pkg1", "pkg2", "pkg3")
pluralize("Will remove {?no/the/the} {pkgs} package{?s}.")

# Multiple quantities
nfiles <- 3; ndirs <- 1
pluralize("Found {nfiles} file{?s} and {ndirs} director{?y/ies}")

# Explicit quantities
nupd <- 3; ntotal <- 10
cli_text("{nupd}/{ntotal} {qty(nupd)} file{?s} {?needs/need} updates")
}) # examplesIf