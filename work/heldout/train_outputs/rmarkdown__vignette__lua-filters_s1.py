# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

# rmarkdown and knitr are R-specific packages for document generation.
# There are no direct 1:1 Python equivalents.
# We create a dummy object to mimic the R structure for the options set.

# r2py:entity:opts_chunk$set
class KnitrDummy:
    class OptsChunk:
        def set(self, **kwargs):
            pass
    opts_chunk = OptsChunk()

knitr = KnitrDummy()

# suppressPackageStartupMessages(library(rmarkdown))
pass

# library(rmarkdown)
pass

# r2py:entity:opts_chunk$set
knitr.opts_chunk.set(
    collapse=True,
    comment="#>"
)