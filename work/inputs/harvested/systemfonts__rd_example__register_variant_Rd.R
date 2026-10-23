# r2py crawler metadata
# package: systemfonts
# source_type: rd_example
# topic: register_variant.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\systemfonts\help
# lines: 16

suppressPackageStartupMessages(library(systemfonts))
# Get the default "sans" family
sans <- match_fonts("sans")$path
sans <- system_fonts()$family[system_fonts()$path == sans][1]

# Register a variant of it:
register_variant(
  "sans_ligature",
  sans,
  features = font_feature(ligatures = "discretionary")
)

registry_fonts()

# clean up
clear_registry()