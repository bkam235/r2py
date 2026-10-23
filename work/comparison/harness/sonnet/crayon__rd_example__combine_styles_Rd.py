# Translated from <R script> by r2py v0.3.0
# Model: claude-sonnet-4-6  ScriptMap entities: 10

from colorama import init, Fore, Back, Style

init()

# r2py:entity:alert
def combine_styles(*styles):
    def apply(text):
        result = text
        for style in reversed(styles):
            result = style(result)
        return result
    return apply

def bold(text):
    return f"{Style.BRIGHT}{text}{Style.RESET_ALL}"

def red(text):
    return f"{Fore.RED}{text}{Style.RESET_ALL}"

def bg_cyan(text):
    return f"{Back.CYAN}{text}{Style.RESET_ALL}"

# r2py:entity:alert
alert = combine_styles(bold, red, bg_cyan)
# r2py:entity:cat
print(alert("Warning!"))

# r2py:entity:alert_1
alert = combine_styles(bold, red, bg_cyan)
# r2py:entity:cat_1
print(alert("Warning!"))

# r2py:entity:alert_2
alert = combine_styles(bold, combine_styles(red, bg_cyan))
# r2py:entity:cat_2
print(alert("Warning!"))

# r2py:entity:alert_3
def chain(text):
    return bg_cyan(red(bold(text)))

alert = chain
# r2py:entity:cat_3
print(alert("Warning!"))