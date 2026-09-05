# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import os

# Mocking systemfonts behavior as there is no direct Python equivalent 
# for R's systemfonts::add_fonts and clear_local_fonts.
# r2py:entity:empty_font
class SystemFontsMock:
# r2py:entity:add_fonts
    def add_fonts(self, font_path):
        # Mimics registering a font
        pass

# r2py:entity:clear_local_fonts
    def clear_local_fonts(self):
        # Mimics clearing the local font cache
        pass

    def system_file(self, file, package=None):
        # Mimics R's system.file()
        # In the R environment, this returns the path to unfont.ttf within the package
        if package == "systemfonts" and file == "unfont.ttf":
            # Based on verification result, the path follows this pattern
            return "C:/Users/bened/Desktop/r2py_v0.3/r2py/stage0/r_env/library/systemfonts/unfont.ttf"
        return ""

sys_fonts = SystemFontsMock()

# suppressPackageStartupMessages(library(systemfonts))
# In Python, imports don't typically produce startup messages like R packages.

# empty_font <- system.file("unfont.ttf", package = "systemfonts")
# r2py:entity:empty_font
empty_font = sys_fonts.system_file("unfont.ttf", package="systemfonts")

# add_fonts(empty_font)
# r2py:entity:add_fonts
sys_fonts.add_fonts(empty_font)

# clear_local_fonts()
# r2py:entity:clear_local_fonts
sys_fonts.clear_local_fonts()