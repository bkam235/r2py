# r2py crawler metadata
# package: pillar
# source_type: rd_example
# topic: ctl_new_pillar_list.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pillar\help
# lines: 40

suppressPackageStartupMessages(library(pillar))
if (rlang::is_installed(c("palmerpenguins", "tibble")) && requireNamespace("tibble")) withAutoprint({ # examplesIf
# Simple column
ctl_new_pillar_list(
  tibble::tibble(),
  palmerpenguins::penguins$weight[1:3],
  width = 10
)

# Packed data frame: unknown width
ctl_new_pillar_list(
  tibble::tibble(),
  palmerpenguins::penguins[1:3, ],
  width = NULL
)

# Packed data frame: known width
ctl_new_pillar_list(
  tibble::tibble(),
  palmerpenguins::penguins,
  width = 60
)

# Deeply packed data frame with known width:
# showing only the first sub-column even if the width is sufficient
ctl_new_pillar_list(
  tibble::tibble(),
  tibble::tibble(x = tibble::tibble(b = 1, c = 2), y = 3),
  width = 60
)

# Packed matrix: unknown width
ctl_new_pillar_list(tibble::tibble(), matrix(1:6, ncol = 2), width = NULL)

# Packed matrix: known width
ctl_new_pillar_list(tibble::tibble(), matrix(1:6, ncol = 2), width = 60)

# Packed array
ctl_new_pillar_list(tibble::tibble(), Titanic, width = 60)
}) # examplesIf