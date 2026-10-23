import types

# Simulation of R Environment
class REnv(dict):
    def __repr__(self):
        return f"<environment: {self._name}>"
    
    def __init__(self, name="R_GlobalEnv", parent=None):
        super().__init__()
        self._name = name
        self._parent = parent

# r2py:entity:default
def env():
    """Returns a new empty environment."""
    return REnv(name="empty_env")

def current_env():
    """Returns the simulated global environment."""
    if not hasattr(current_env, "_global"):
        current_env._global = REnv(name="R_GlobalEnv")
    return current_env._global

# r2py:entity:env
def child_env(parent_val=None):
    """Creates a child environment."""
    if isinstance(parent_val, str):
        # Simulate namespace environments like "base"
        return REnv(name=parent_val)
    parent = parent_val if isinstance(parent_val, REnv) else current_env()
    return REnv(name="child_env", parent=parent)

# r2py:entity:f
class RFormula:
    def __init__(self, expr, env_val=None):
        self.expr = expr
        self.env = env_val
    def __repr__(self):
        return f"~{self.expr}"

# r2py:entity:get_env_2
def quo(expr):
    """Simulates R's quo() capturing expression and environment."""
    return {"expr": expr, "env": current_env()}

# r2py:entity:get_env
def get_env(obj, default=None):
    """Translates get_env logic."""
    # Closure functions
    if isinstance(obj, types.FunctionType):
        if hasattr(obj, "_r_env"):
            return obj._r_env
        return current_env()
    
    # RFunction wrapper (simulating closure with env)
    if isinstance(obj, RFunction):
        return obj.env

    # Quosures (dicts with 'env')
    if isinstance(obj, dict) and "env" in obj:
        return obj["env"]
    
    # Formulas
    if isinstance(obj, RFormula):
        return obj.env if obj.env is not None else default

    # Environments
    if isinstance(obj, REnv):
        return obj

    return default

class RFunction:
    """Wrapper to simulate R closure with a specific environment."""
    def __init__(self, func, env_val):
        self.func = func
        self.env = env_val
    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
    def __repr__(self):
        # Simulate the R output format for functions
        return f"function () \nNULL\n<environment: {self.env}>"

# r2py:entity:set_env
def set_env(obj, new_env_val):
    """Translates set_env. No side effects on the original object."""
    if isinstance(obj, RFormula):
        return RFormula(obj.expr, new_env_val)
    
    if isinstance(obj, (types.FunctionType, RFunction)):
        actual_func = obj.func if isinstance(obj, RFunction) else obj
        return RFunction(actual_func, new_env_val)

    return new_env_val

# r2py:entity:identical
def identical(x, y):
    """Equivalent to R's identical()."""
    return x is y

def format_bool(val):
    return "TRUE" if val else "FALSE"

# --- Execution ---

# Environment of closure functions:
# r2py:entity:fn
def _fn_impl():
    return "foo"
fn = _fn_impl
# r2py:entity:get_env
print(get_env(fn))

# Or of quosures or formulas:
# r2py:entity:get_env_1
formula_obj = RFormula("foo", env_val=current_env())
print(get_env(formula_obj))
# r2py:entity:get_env_2
print(get_env(quo("foo")))

# Provide a default in case the object doesn't bundle an environment.
# r2py:entity:f
f = RFormula("foo") # Unevaluated formulas in R don't have an env yet
# r2py:entity:default
default = env()
# r2py:entity:identical
print(f"[1] {format_bool(identical(get_env(f, default), default))}")

# set_env() can be used to set the enclosure of functions and formulas.
# r2py:entity:env
env_val = child_env("base")
# r2py:entity:fn_1
def _fn_null():
    return None
fn = set_env(_fn_null, env_val)

# That function now has `env_val` as enclosure:
# r2py:entity:identical_1
print(f"[1] {format_bool(identical(get_env(fn), env_val))}")
# r2py:entity:identical_2
print(f"[1] {format_bool(identical(get_env(fn), current_env()))}")

# set_env() does not work by side effect.
# r2py:entity:other_env
other_env = child_env(None)
# r2py:entity:set_env
res = set_env(fn, other_env)
print(res) 
# r2py:entity:identical_3
print(f"[1] {format_bool(identical(get_env(fn), other_env))}")

# Since set_env() returns a new function, reassign the result:
# r2py:entity:fn_2
fn = set_env(fn, other_env)
# r2py:entity:identical_4
print(f"[1] {format_bool(identical(get_env(fn), other_env))}")