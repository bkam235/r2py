# r2py crawler metadata
# package: tidyr
# source_type: rd_example
# topic: hoist.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\help
# lines: 28

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

# Extract only specified components
df |> hoist(metadata,
  "species",
  first_film = list("films", 1L),
  third_film = list("films", 3L)
)