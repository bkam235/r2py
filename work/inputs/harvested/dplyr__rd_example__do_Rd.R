# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: do.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 31

suppressPackageStartupMessages(library(dplyr))
# do() with unnamed arguments becomes reframe() or summarise()
# . becomes pick()
by_cyl <- mtcars |> group_by(cyl)
by_cyl |> do(head(., 2))
# ->
by_cyl |> reframe(head(pick(everything()), 2))
by_cyl |> slice_head(n = 2)

# Can refer to variables directly
by_cyl |> do(mean = mean(.$vs))
# ->
by_cyl |> summarise(mean = mean(vs))

# do() with named arguments becomes nest_by() + mutate() & list()
models <- by_cyl |> do(mod = lm(mpg ~ disp, data = .))
# ->
models <- mtcars |>
  nest_by(cyl) |>
  mutate(mod = list(lm(mpg ~ disp, data = data)))
models |> summarise(rsq = summary(mod)$r.squared)

# use broom to turn models into data
models |> do(data.frame(
  var = names(coef(.$mod)),
  coef(summary(.$mod)))
)
if (requireNamespace("broom", quietly = TRUE)) withAutoprint({ # examplesIf
# ->
models |> reframe(broom::tidy(mod))
}) # examplesIf