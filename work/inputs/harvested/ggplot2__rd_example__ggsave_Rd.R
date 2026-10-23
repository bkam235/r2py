# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: ggsave.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 32

suppressPackageStartupMessages(library(ggplot2))
ggplot(mtcars, aes(mpg, wt)) +
  geom_point()

# here, the device is inferred from the filename extension
ggsave("mtcars.pdf")
ggsave("mtcars.png")

# setting dimensions of the plot
ggsave("mtcars.pdf", width = 4, height = 4)
ggsave("mtcars.pdf", width = 20, height = 20, units = "cm")

# passing device-specific arguments to '...'
ggsave("mtcars.pdf", colormodel = "cmyk")

# delete files with base::unlink()
unlink("mtcars.pdf")
unlink("mtcars.png")

# specify device when saving to a file with unknown extension
# (for example a server supplied temporary file)
file <- tempfile()
ggsave(file, device = "pdf")
unlink(file)

# save plot to file without using ggsave
p <-
  ggplot(mtcars, aes(mpg, wt)) +
  geom_point()
png("mtcars.png")
print(p)
dev.off()