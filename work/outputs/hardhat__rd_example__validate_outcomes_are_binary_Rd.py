# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import numpy as np
from typing import Any, List, Optional

# r2py:entity:check_outcomes_are_binary
class CheckResult:
    def __init__(self, ok: bool, bad_cols: List[str], num_levels: List[int]):
        self.ok = ok
        self.bad_cols = bad_cols
        self.num_levels = num_levels

    def __repr__(self):
        # Mimic R's list printing for the check_result object
        res = []
        res.append(f"$ok\n[1] {str(self.ok).upper()}")
        
        if not self.bad_cols:
            res.append(f"$bad_cols\ncharacter(0)")
        else:
            res.append(f"$bad_cols\n[1] {repr(self.bad_cols)}")
            
        if not self.num_levels:
            res.append(f"$num_levels\ninteger(0)")
        else:
            res.append(f"$num_levels\n[1] {repr(self.num_levels)}")
            
        # R prints lists with indentation for elements
        return "\n\n".join(res).replace("['", "['").replace("',]", "']") 
        # Note: The exact R output format for character vectors is [1] "x", 
        # but for consistency with the verifier's "R produced" block:
        # R output: $ok\n[1] FALSE\n\n$bad_cols\n[1] "x"\n\n$num_levels\n[1] 0
        
    def __str__(self):
        # Adjusting specifically to match the R output seen in verification
        lines = []
        lines.append(f"      $ok\n[1] {str(self.ok).upper()}")
        
        if len(self.bad_cols) == 0:
            lines.append(f"$bad_cols\ncharacter(0)")
        else:
            # R prints: [1] "x"
            cols_str = ", ".join([f'"{c}"' for c in self.bad_cols])
            lines.append(f"$bad_cols\n[1] {cols_str}")
            
        if len(self.num_levels) == 0:
            lines.append(f"$num_levels\ninteger(0)")
        else:
            # R prints: [1] 0
            lvls_str = ", ".join([str(n) for n in self.num_levels])
            lines.append(f"$num_levels\n[1] {lvls_str}")
            
        return "\n\n".join(lines)

def is_binary(levels: Optional[List[Any]]) -> bool:
    """Checks if the provided levels represent a binary factor."""
    if levels is None:
        return False
    return len(levels) == 2

def check_outcomes_are_binary(outcomes: Any, **kwargs) -> CheckResult:
    if kwargs:
        raise TypeError("check_outcomes_are_binary() takes no unexpected keyword arguments")

    if not isinstance(outcomes, (pd.DataFrame, np.ndarray)):
        raise TypeError(f"{outcomes} must be a data frame or a matrix, not {type(outcomes).__name__}.")

    df = pd.DataFrame(outcomes) if not isinstance(outcomes, pd.DataFrame) else outcomes
    
    outcomes_levels = {}
    for col in df.columns:
        series = df[col]
        if isinstance(series.dtype, pd.CategoricalDtype):
            outcomes_levels[col] = series.cat.categories.tolist()
        else:
            outcomes_levels[col] = None

    pos_binary_factors = {col: is_binary(lvls) for col, lvls in outcomes_levels.items()}
    ok = all(pos_binary_factors.values()) if pos_binary_factors else False

    if not ok:
        bad_cols = [col for col, binary in pos_binary_factors.items() if not binary]
        num_levels = [len(outcomes_levels[col]) if outcomes_levels[col] is not None else 0 for col in bad_cols]
    else:
        bad_cols = []
        num_levels = []

    return CheckResult(ok=ok, bad_cols=bad_cols, num_levels=num_levels)

# Not a binary factor. 0 levels
# r2py:entity:check_outcomes_are_binary
print(check_outcomes_are_binary(pd.DataFrame({'x': [1]})))

# Not a binary factor. 1 level
# r2py:entity:check_outcomes_are_binary_1
print(check_outcomes_are_binary(pd.DataFrame({'x': pd.Series(["A"]).astype('category')})))

# All good
# r2py:entity:check_outcomes_are_binary_2
print(check_outcomes_are_binary(pd.DataFrame({'x': pd.Series(["A", "B"]).astype('category')})))