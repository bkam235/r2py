# Translated from <R script> by r2py v0.3.0
# Model: claude-opus-4-6  ScriptMap entities: 10

from colorama import init, Fore, Back, Style

init()

# r2py:entity:alert
def combine_styles(*styles):
    def styled(text):
        prefix = "".join(styles)
        return f"{prefix}{text}{Style.RESET_ALL}"
    return styled

bold = Style.BRIGHT
red = Fore.RED
bgCyan = Back.CYAN

alert = combine_styles(bold, red, bgCyan)
# r2py:entity:cat
print(alert("Warning!"))

# r2py:entity:alert_1
alert = combine_styles(bold, red, bgCyan)
# r2py:entity:cat_1
print(alert("Warning!"))

# r2py:entity:alert_2
alert = combine_styles(bold, combine_styles(red, bgCyan)("")[:-len(Style.RESET_ALL)])
# r2py:entity:cat_2
print(combine_styles(bold, red, bgCyan)("Warning!"))

# r2py:entity:alert_3
alert = combine_styles(bold, red, bgCyan)
# r2py:entity:cat_3
print(alert("Warning!"))