# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 6

# r2py:entity:large
def large(x):
    return f'{{\\Large{{\\bfseries {x}}}}}'

# r2py:entity:italic
def italic(x):
    return f'{{\\emph{{ {x}}}}}'

# r2py:entity:bold
def bold(x):
    return f'{{\\bfseries {x}}}'

# r2py:entity:red
def red(x):
    return f'{{\\color{{red}} {x}}}'