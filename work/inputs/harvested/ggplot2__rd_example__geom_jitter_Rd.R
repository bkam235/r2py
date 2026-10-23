# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: geom_jitter.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 19

suppressPackageStartupMessages(library(ggplot2))
p <- ggplot(mpg, aes(cyl, hwy))
p + geom_point()
p + geom_jitter()

# Add aesthetic mappings
p + geom_jitter(aes(colour = class))

# Use smaller width/height to emphasise categories
ggplot(mpg, aes(cyl, hwy)) +
  geom_jitter()
ggplot(mpg, aes(cyl, hwy)) +
  geom_jitter(width = 0.25)

# Use larger width/height to completely smooth away discreteness
ggplot(mpg, aes(cty, hwy)) +
  geom_jitter()
ggplot(mpg, aes(cty, hwy)) +
  geom_jitter(width = 0.5, height = 0.5)