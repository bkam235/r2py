# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_pca.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 22

suppressPackageStartupMessages(library(recipes))
rec <- recipe(~., data = USArrests)
pca_trans <- rec |>
  step_normalize(all_numeric()) |>
  step_pca(all_numeric(), num_comp = 3)
pca_estimates <- prep(pca_trans, training = USArrests)
pca_data <- bake(pca_estimates, USArrests)

rng <- extendrange(c(pca_data$PC1, pca_data$PC2))
plot(pca_data$PC1, pca_data$PC2,
  xlim = rng, ylim = rng
)

with_thresh <- rec |>
  step_normalize(all_numeric()) |>
  step_pca(all_numeric(), threshold = .99)
with_thresh <- prep(with_thresh, training = USArrests)
bake(with_thresh, USArrests)

tidy(pca_trans, number = 2)
tidy(pca_estimates, number = 2)
tidy(pca_estimates, number = 2, type = "variance")