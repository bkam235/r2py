# r2py crawler metadata
# package: crayon
# source_type: rd_example
# topic: combine_styles.Rd
# Translated from R to Python

from colorama import Fore, Back, Style, init

# Initialize colorama for cross-platform terminal colors
init(autoreset=True)

# Create alert style combining bold, red text, and cyan background
alert_text = f"{Style.BRIGHT}{Fore.RED}{Back.CYAN}Warning!{Style.RESET_ALL}"
print(alert_text)

# Alternative: using individual styles combined
alert_text2 = f"{Style.BRIGHT}{Fore.RED}{Back.CYAN}Warning!{Style.RESET_ALL}"
print(alert_text2)

# Composite style
alert_text3 = f"{Style.BRIGHT}{Fore.RED}{Back.CYAN}Warning!{Style.RESET_ALL}"
print(alert_text3)

# Shorter notation using f-strings
alert_text4 = f"{Style.BRIGHT}{Fore.RED}{Back.CYAN}Warning!{Style.RESET_ALL}"
print(alert_text4)
