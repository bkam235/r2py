# r2py crawler metadata
# package: hardhat
# source_type: vignette
# topic: package_s23
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\doc\package.R
# lines: 32

suppressPackageStartupMessages(library(hardhat))
try({
# `new_data` isn't a data frame
predict(model, penguins$species)

# Missing a required column
predict(model, subset(penguins, select = -body_mass_g))

# In this case, 'species' is a character, 
# but can be losslessy converted to a factor.
# That happens for you automatically and silently.
penguins_chr_species <- transform(penguins, species = as.character(species))

predict(model, penguins_chr_species)

# Slightly different from above. Here, 'species' is a character, 
# AND has an extra unexpected factor level. It is 
# removed with a warning, but you still get a factor 
# with the correct levels
penguins_chr_bad_species <- penguins_chr_species
penguins_chr_bad_species$species[1] <- "new_level"

predict(model, penguins_chr_bad_species)

# This case throws an error.
# Here, 'species' is a double and
# when it should have been a factor.
# You can't cast a double to a factor!
penguins_dbl_species <- transform(penguins, species = 1)

predict(model, penguins_dbl_species)
})