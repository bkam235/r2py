# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import ast

# r2py:entity:valid_syntax
def valid_syntax(code):
    if isinstance(code, list):
        for item in code:
            try:
                ast.parse(item)
                print(True)
            except SyntaxError:
                print(False)
    else:
        try:
            ast.parse(code)
            print(True)
        except SyntaxError:
            print(False)

valid_syntax("1+1")
# r2py:entity:valid_syntax_1
valid_syntax("1+")
# r2py:entity:valid_syntax_2
valid_syntax(["if True: 1+1", "else: 2+2"])