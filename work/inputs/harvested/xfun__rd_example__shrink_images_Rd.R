# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: shrink_images.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 10

suppressPackageStartupMessages(library(xfun))
if (xfun::loadable('magick')) {
f = xfun:::all_files("[.](png|jpe?g)$", R.home("doc"))
file.copy(f, tempdir())
f = file.path(tempdir(), basename(f))
magick::image_info(magick::image_read(f))  # some widths are larger than 300
xfun::shrink_images(300, files = f)
magick::image_info(magick::image_read(f))  # all widths <= 300 now
file.remove(f)
}