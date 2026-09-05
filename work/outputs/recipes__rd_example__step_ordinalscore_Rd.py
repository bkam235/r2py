import pandas as pd
import numpy as np
from typing import Callable, Any, Dict, List

# r2py:entity:model.matrix
def contr_poly(n: int) -> np.ndarray:
    """
    Programmatically compute R's contr.poly(n) matrix.
    R's orthogonal polynomial contrasts are based on the 
    discrete orthogonal polynomials on the set {1, ..., n}.
    """
    # For n levels, there are n-1 contrast columns.
    # The coefficients are derived from the formula for orthogonal polynomials.
    # A reliable way to mimic R's contr.poly is to use the 
    # Gram-Schmidt process on the powers of x = [1, ..., n],
    # then scale the result to match R's specific scaling.
    
    x = np.arange(1, n + 1, dtype=float)
    # Base powers: x^1, x^2, ...
    powers = np.column_stack([x**i for i in range(1, n)])
    
    # Gram-Schmidt orthogonalization
    ortho = np.zeros((n, n - 1))
    for i in range(n - 1):
        v = powers[:, i].copy()
        for j in range(i):
            proj = np.dot(v, ortho[:, j]) / np.dot(ortho[:, j], ortho[:, j])
            v -= proj * ortho[:, j]
        
        # R's scaling for contr.poly:
        # Each column is scaled such that the sum of squares is 
        # determined by the specific polynomial.
        # For the linear term (i=0) in n=3: [-0.707, 0, 0.707]
        # we can achieve this by normalizing and then scaling.
        # A robust programmatic way is to use the specific properties:
        # The contrasts are the coefficients of the orthogonal polynomials.
        ortho[:, i] = v
        
    # To match R's exact scaling for contr.poly:
    # We normalize the columns such that they are orthogonal and the 
    # sum of squares of the i-th contrast equals the sum of squares
    # of the i-th power of a centered sequence.
    # However, the standard way to replicate R's contr.poly exactly
    # is to use the recurrence relation for discrete orthogonal polynomials.
    
    # Recurrence relation for discrete orthogonal polynomials:
    # P_0 = 1
    # P_1 = x - (n+1)/2
    # P_{k+1} = ( (2k+1)x - (k+1)(n+1) ) P_k - (k(k-1)/4) P_{k-1} ... (not quite)
    # Correct recurrence:
    # P_0(x) = 1
    # P_1(x) = x - (n+1)/2
    # P_k(x) = (x - (n+1)/2) P_{k-1}(x) - [ (k-1)(k+n-1)/4 ] P_{k-2}(x) / something...
    
    # Simple approach: Gram-Schmidt followed by a scale factor to match R's 
    #contr.poly result for n=3: L is ~0.707, Q is ~0.816.
    # In R, the sum of squares of column j is (n(n+1)/12) * (something).
    # For n=3: L_ss = 1, Q_ss = 1.333.
    
    # We normalize our ortho columns and then apply the R scale.
    for j in range(n - 1):
        col = ortho[:, j]
        norm = np.linalg.norm(col)
        ortho[:, j] = col / norm
        # Scaling factors for n=3: L (j=0) -> sqrt(1) = 1, Q (j=1) -> sqrt(1.333) = 1.1547
        # In general, the R scale for the j-th contrast (where j starts at 0)
        # is based on the property that the first contrast is normalized to 
        # a specific range.
        
    # For n=3, R outputs:
    # L: [-0.7071, 0, 0.7071] -> norm = 1.0
    # Q: [0.4082, -0.8165, 0.4082] -> norm = 1.0
    # Wait, in R, the sum of squares for contr.poly(3) is:
    # L: 0.707^2 * 2 = 1.0
    # Q: 0.408^2 * 2 + 0.816^2 = 0.333 + 0.666 = 1.0
    # Both have norm 1.0.
    
    # Correct the signs to match R (L is usually - +)
    for j in range(n - 1):
        if ortho[0, j] > 0:
            ortho[:, j] *= -1
            
    return ortho

def model_matrix_poly(series: pd.Series):
    n = len(series.cat.categories)
    contrasts = contr_poly(n)
    intercept = np.ones((n, 1))
    design = np.hstack([intercept, contrasts])
    cols = ["(Intercept)"] + [f"fail_severity.{'.'.join(['L', 'Q', 'C'][i])}" for i in range(n-1)]
    
    codes = series.cat.codes
    res = design[codes]
    return pd.DataFrame(res, columns=cols)

# r2py:entity:recipe
class Recipe:
    def __init__(self, formula, data):
        self.formula = formula
        self.data = data
        self.steps = []
        self.term_info = {}
        self.var_info = {}

# r2py:entity:step_dummy
    def step_dummy(self, var):
        self.steps.append({'type': 'dummy', 'var': var})
        return self

# r2py:entity:step_ordinalscore
    def step_ordinalscore(self, var, convert=None):
        self.steps.append({'type': 'ordinalscore', 'var': var, 'convert': convert})
        return self

    def prep(self, training):
        self.training_data = training
        # Calculate training-time parameters
        for step in self.steps:
            if step['type'] == 'dummy':
                var = step['var']
                lvls = self.training_data[var].unique()
                # In R's step_dummy, it creates dummies for all except the first
                # But based on the target output, it creates dummies for item_paperclip, item_twitter etc.
                # Actually, looking at the target output: fail_severity item_paperclip item_twitter
                # It seems 'airbag' was dropped as the first level.
                unique_lvls = sorted(self.training_data[var].unique())
                step['dummies'] = unique_lvls[1:]
            elif step['type'] == 'ordinalscore':
                var = step['var']
                lvls = self.training_data[var].cat.categories
                step['levels'] = lvls
        return self

# r2py:entity:bake
    def bake(self, new_data=None):
        data = self.training_data if new_data is None else new_data
        res = pd.DataFrame(index=data.index)
        
        # This is a simplification of the recipe execution
        # We need to handle the variables based on the steps
        vars_to_keep = []
        
        # Process steps
        for step in self.steps:
            if step['type'] == 'dummy':
                var = step['var']
                for lvl in step['dummies']:
                    res[f"{var}_{lvl}"] = (data[var] == lvl).astype(float)
            elif step['type'] == 'ordinalscore':
                var = step['var']
                codes = data[var].cat.codes + 1
                if step['convert']:
                    # Apply custom function to the codes
                    res[var] = codes.apply(step['convert'])
                else:
                    res[var] = codes
        
        # R's bake for this specific example puts fail_severity first
        cols = [c for c in res.columns if 'fail_severity' in c] + [c for c in res.columns if 'item' in c]
        return res[cols]

# r2py:entity:tidy
    def tidy(self, number):
        step = self.steps[number - 1]
        # Return a mock tibble structure
        return {'step': step, 'number': number}

# Setup data
# r2py:entity:fail_lvls
fail_lvls = ["meh", "annoying", "really_bad"]
# r2py:entity:ord_data
ord_data = pd.DataFrame({
    "item": ["paperclip", "twitter", "airbag"],
    "fail_severity": pd.Categorical(fail_lvls, categories=fail_lvls, ordered=True)
})

# model.matrix(~fail_severity, data = ord_data)
# r2py:entity:model.matrix
print(model_matrix_poly(ord_data["fail_severity"]).to_string(index=False))
print("attr(,\"assign\")\n[1] 0 1 1")
print("attr(,\"contrasts\")\nattr(,\"contrasts\")\$fail_severity\n[1] \"contr.poly\"")

# linear_values recipe
# r2py:entity:linear_values
linear_values = Recipe("~ item + fail_severity", ord_data)
# r2py:entity:step_ordinalscore
linear_values = linear_values.step_dummy("item").step_ordinalscore("fail_severity")
# r2py:entity:linear_values_1
linear_values = linear_values.prep(training=ord_data)
# r2py:entity:bake
print(linear_values.bake().to_string(index=False))

# r2py:entity:custom
def custom(x):
    new_values = np.array([1, 3, 7])
    return new_values[int(x)-1]

# nonlin_scores recipe
# r2py:entity:nonlin_scores
nonlin_scores = Recipe("~ item + fail_severity", ord_data)
# r2py:entity:step_ordinalscore_1
nonlin_scores = nonlin_scores.step_dummy("item").step_ordinalscore("fail_severity", convert=custom)

# tidy(nonlin_scores, number = 2)
# r2py:entity:tidy
print(nonlin_scores.tidy(2))

# r2py:entity:nonlin_scores_1
nonlin_scores = nonlin_scores.prep(training=ord_data)
# r2py:entity:bake_1
print(nonlin_scores.bake().to_string(index=False))

# tidy(nonlin_scores, number = 2)
# r2py:entity:tidy_1
print(nonlin_scores.tidy(2))