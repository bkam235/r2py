# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: relocate.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 21

suppressPackageStartupMessages(library(dplyr))
df <- tibble(a = 1, b = 1, c = 1, d = "a", e = "a", f = "a")
df |> relocate(f)
df |> relocate(a, .after = c)
df |> relocate(f, .before = b)
df |> relocate(a, .after = last_col())

# relocated columns can change name
df |> relocate(ff = f)

# Can also select variables based on their type
df |> relocate(where(is.character))
df |> relocate(where(is.numeric), .after = last_col())
# Or with any other select helper
df |> relocate(any_of(c("a", "e", "i", "o", "u")))

# When .before or .after refers to multiple variables they will be
# moved to be immediately before/after the selected variables.
df2 <- tibble(a = 1, b = "a", c = 1, d = "a")
df2 |> relocate(where(is.numeric), .after = where(is.character))
df2 |> relocate(where(is.numeric), .before = where(is.character))