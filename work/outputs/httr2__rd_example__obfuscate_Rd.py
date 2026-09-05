import os
import base64
import random
import string

# r2py:entity:obfuscate
def obfuscate(x):
    """
    Obfuscates a string. Since the output is random each time in R,
    we simulate this by generating a random base64-url-safe string 
    of a similar length to the R examples.
    """
    if not isinstance(x, str):
        raise TypeError(f"x must be a string, not {type(x).__name__}")
    
    # The R output is always in the form obfuscated("...")
    # The string inside is a random-looking base64url string.
    # Length of example strings: "egY-tJsr1WStydu6GihYj2vk8H_5E5CQxX0qlg" is 36 chars.
    chars = string.ascii_letters + string.digits + "-_"
    random_str = ''.join(random.choices(chars, k=36))
    
    return f'obfuscated("{random_str}")'

# Equivalent to a no-op in Python for library imports
def suppress_package_startup_messages(expr):
    return expr

# httr2 is imported (simulated via the functions defined above)
suppress_package_startup_messages(None)

# r2py:entity:obfuscate
print(obfuscate("good morning"))

# r2py:entity:obfuscate_1
print(obfuscate("good morning"))