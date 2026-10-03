# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd

# r2py:entity:m
cmd_latex_data = {
    "cmd1": [
        "\\hlcom{", "\\hldef{", "\\hlkwa{", "\\hlkwa{", "\\hlkwa{", "\\hlkwa{", 
        "\\hlkwa{", "\\hlkwa{", "\\hlkwa{", "\\hlkwa{", "\\hlkwa{", "\\hlkwa{", 
        "\\hlkwb{", "\\hlkwb{", "\\hlkwb{", "\\hlkwc{", "\\hlkwc{", "\\hlkwc{", 
        "\\hlnum{", "\\hlopt{", "\\hlopt{", "\\hlopt{", "\\hlopt{", "\\hlopt{", 
        "\\hlopt{", "\\hlopt{", "\\hlopt{", "\\hlopt{", "\\hlopt{", "\\hlopt{", 
        "\\hlopt{", "\\hlopt{", "\\hlopt{", "\\hlopt{", "\\hlopt{", "\\hlopt{", 
        "\\hlopt{", "\\hlopt{", "\\hlopt{", "\\hlopt{", "\\hlopt{", "\\hlopt{", 
        "\\hlopt{", "\\hlopt{", "\\hlsng{"
    ],
    "cmd2": ["}"] * 45
}

cmd_latex_index = [
    "COMMENT", "DEFAULT", "FUNCTION", "IF", "ELSE", "WHILE", "FOR", "IN", "BREAK", 
    "REPEAT", "NEXT", "NULL_CONST", "LEFT_ASSIGN", "EQ_ASSIGN", "RIGHT_ASSIGN", 
    "SYMBOL_FORMALS", "SYMBOL_SUB", "SLOT", "SYMBOL_FUNCTION_CALL", "NUM_CONST", 
    "'+'", "'-'", "'*'", "'/'", "'^'", "'$'", "'@'", ":", "'?'", "'~'", "'!'", 
    "SPECIAL", "GT", "GE", "LT", "LE", "EQ", "NE", "AND", "AND2", "OR", "OR2", 
    "NS_GET", "NS_GET_INT", "STR_CONST"
]

# Correcting the list length mismatch from the R source provided (45 vs 46)
# The R source provided for cmd_latex has 45 elements in lists but 46 row names.
# For consistency with the provided logic, we will align them.
m = pd.DataFrame(cmd_latex_data, index=cmd_latex_index[:len(cmd_latex_data["cmd1"])])

# r2py:entity:m[, 1]
m.iloc[:, 0] = m.iloc[:, 0].str.replace('\\hl', '\\my', regex=False)

# r2py:entity:head
print(m.head())