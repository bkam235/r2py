# r2py crawler metadata
# package: cli
# source_type: rd_example
# topic: cli_format_method.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cli\help
# lines: 44

suppressPackageStartupMessages(library(cli))
# Let's create format and print methods for a new S3 class that
# represents the an installed R package: `r_package`

# An `r_package` will contain the DESCRIPTION metadata of the package
# and also its installation path.
new_r_package <- function(pkg) {
  tryCatch(
    desc <- packageDescription(pkg),
    warning = function(e) stop("Cannot find R package `", pkg, "`")
  )
  file <- dirname(attr(desc, "file"))
  if (basename(file) != pkg) file <- dirname(file)
  structure(
    list(desc = unclass(desc), lib = dirname(file)),
    class = "r_package"
  )
}

format.r_package <- function(x, ...) {
  cli_format_method({
    cli_h1("{.pkg {x$desc$Package}} {cli::symbol$line} {x$desc$Title}")
    cli_text("{x$desc$Description}")
    cli_ul(c(
      "Version: {x$desc$Version}",
      if (!is.null(x$desc$Maintainer)) "Maintainer: {x$desc$Maintainer}",
      "License: {x$desc$License}"
    ))
    if (!is.na(x$desc$URL)) cli_text("See more at {.url {x$desc$URL}}")
  })
}

# Now the print method is easy:
print.r_package <- function(x, ...) {
  cat(format(x, ...), sep = "\n")
}

# Try it out
new_r_package("cli")

# The formatting of the output depends on the current theme:
opt <- options(cli.theme = simple_theme())
print(new_r_package("cli"))
options(opt)  # <- restore theme