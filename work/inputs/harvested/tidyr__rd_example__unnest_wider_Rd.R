# r2py crawler metadata
# package: tidyr
# source_type: rd_example
# topic: unnest_wider.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\help
# lines: 52

suppressPackageStartupMessages(library(tidyr))
df <- tibble(
  character = c("Toothless", "Dory"),
  metadata = list(
    list(
      species = "dragon",
      color = "black",
      films = c(
        "How to Train Your Dragon",
        "How to Train Your Dragon 2",
        "How to Train Your Dragon: The Hidden World"
      )
    ),
    list(
      species = "blue tang",
      color = "blue",
      films = c("Finding Nemo", "Finding Dory")
    )
  )
)
df

# Turn all components of metadata into columns
df |> unnest_wider(metadata)

# Choose not to simplify list-cols of length-1 elements
df |> unnest_wider(metadata, simplify = FALSE)
df |> unnest_wider(metadata, simplify = list(color = FALSE))

# You can also widen unnamed list-cols:
df <- tibble(
  x = 1:3,
  y = list(NULL, 1:3, 4:5)
)
# but you must supply `names_sep` to do so, which generates automatic names:
df |> unnest_wider(y, names_sep = "_")

# 0-length elements ---------------------------------------------------------
# The defaults of `unnest_wider()` treat empty types (like `list()`) as `NULL`.
json <- list(
  list(x = 1:2, y = 1:2),
  list(x = list(), y = 3:4),
  list(x = 3L, y = list())
)

df <- tibble(json = json)
df |>
  unnest_wider(json)

# To instead enforce strict vctrs typing rules, use `strict`
df |>
  unnest_wider(json, strict = TRUE)