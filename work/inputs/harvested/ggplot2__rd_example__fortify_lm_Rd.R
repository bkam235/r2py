# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: fortify.lm.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 18

suppressPackageStartupMessages(library(ggplot2))
if (require("broom")) withAutoprint({ # examplesIf
mod <- lm(mpg ~ wt, data = mtcars)

# Show augmented model
head(augment(mod))
head(fortify(mod))

# Using augment to convert model to ready-to-plot data
ggplot(augment(mod), aes(.fitted, .resid)) +
  geom_point() +
  geom_hline(yintercept = 0) +
  geom_smooth(se = FALSE)

# Colouring by original data not included in the model
ggplot(augment(mod, mtcars), aes(.fitted, .std.resid, colour = factor(cyl))) +
  geom_point()
}) # examplesIf