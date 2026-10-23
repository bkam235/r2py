import pandas as pd
import numpy as np

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/recipes__rd_example__formula_recipe_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'recipes__rd_example__formula_recipe_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# Ensure iris is a DataFrame
if 'iris' in globals() and isinstance(iris, dict):
    iris = pd.DataFrame(iris)

# r2py:entity:iris_rec
class Recipe:
    def __init__(self, formula_str, data):
        self.formula_str = formula_str
        self.template = data.copy()
        self.steps = []
        self.trained = False
        
        # Simple formula parsing: LHS ~ RHS
        lhs_str, rhs_str = formula_str.split('~')
        lhs_vars = [v.strip() for v in lhs_str.split('+')]
        
        if rhs_str.strip() == '.':
            rhs_vars = [col for col in data.columns if col not in lhs_vars]
        else:
            rhs_vars = [v.strip() for v in rhs_str.split('+')]
            rhs_vars = [v for v in rhs_vars if v not in lhs_vars]
            
        self.var_info = pd.DataFrame({
            'variable': rhs_vars + lhs_vars,
            'role': ['predictor'] * len(rhs_vars) + ['outcome'] * len(lhs_vars),
            'source': 'original'
        })

    def prep(self):
        # In this simple implementation, prep marks the recipe as trained
        self.trained = True
        return self

    def get_formula(self):
        if not self.trained:
            raise RuntimeError("The recipe must be prepped before the formula can be computed.")
        
        predictors = self.var_info[self.var_info['role'] == 'predictor']['variable'].tolist()
        outcomes = self.var_info[self.var_info['role'] == 'outcome']['variable'].tolist()
        
        lhs = " + ".join(outcomes) if outcomes else ""
        rhs = " + ".join(predictors) if predictors else "1"
        return f"{lhs} ~ {rhs}"

# r2py:entity:recipe
def recipe(formula_str, data):
    return Recipe(formula_str, data)

# r2py:entity:step_center
def step_center(rec, *args, **kwargs):
    # In R, step_center adds a step to the recipe
    rec.steps.append('center')
    return rec

def all_numeric():
    return 'all_numeric'

# r2py:entity:prep
def prep(rec):
    return rec.prep()

# r2py:entity:formula
def formula(rec):
    # R's formula(recipe) returns the formula object
    res = rec.get_formula()
    print(res)
    # Print environment-like string to match R output
    print(f"<environment: {id(rec)}>")
    return res

# Execution
# formula(recipe(Species + Sepal.Length ~ ., data = iris) |> prep())
# r2py:entity:recipe
rec1 = recipe("Species + Sepal.Length ~ .", iris)
# r2py:entity:prep
rec1 = prep(rec1)
# r2py:entity:formula
formula(rec1)

# iris_rec <- recipe(Species ~ ., data = iris) |> step_center(all_numeric()) |> prep()
# r2py:entity:iris_rec
iris_rec = recipe("Species ~ .", iris)
# r2py:entity:step_center
iris_rec = step_center(iris_rec, all_numeric())
iris_rec = prep(iris_rec)

# formula(iris_rec)
# r2py:entity:formula_1
formula(iris_rec)