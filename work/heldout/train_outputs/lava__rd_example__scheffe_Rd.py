# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/lava__rd_example__scheffe_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'lava__rd_example__scheffe_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
import matplotlib.pyplot as plt

# r2py:entity:d2
def scheffe(model, newdata, level=0.95):
    """
    Implementation of the scheffe function from the lava package.
    """
    # df <- model$df.residual
    df = model.df_resid
    # p <- model$rank
    p = len(model.params) - 1 if 'const' in model.model.exog_names else len(model.params)
    # R's lm rank for y ~ x is typically 2 (intercept + slope)
    p = model.df_model + 1 # For simple linear regression y ~ x
    
    alpha = 1 - level
    # scheffe.crit <- sqrt(p * qf(1 - alpha, p, df))
    scheffe_crit = np.sqrt(p * stats.f.ppf(1 - alpha, p, df))
    
    # ci <- predict(model, newdata, interval = "confidence", level = level)
    X_new = sm.add_constant(newdata['x'], has_constant='add')
    prediction = model.get_prediction(X_new)
    ci_frame = prediction.summary_frame(alpha=alpha)
    
    # ci[, 1] is fit, ci[, 2] is lwr, ci[, 3] is upr
    fit = ci_frame['mean'].values
    lwr = ci_frame['mean_ci_lower'].values
    upr = ci_frame['mean_ci_upper'].values
    
    # delta <- scheffe.crit/qt(1 - alpha/2, df)
    delta = scheffe_crit / stats.t.ppf(1 - alpha/2, df)
    
    # ci[, 2] <- ci[, 1] - (ci[, 1] - ci[, 2]) * delta
    # ci[, 3] <- ci[, 1] + (ci[, 3] - ci[, 1]) * delta
    new_lwr = fit - (fit - lwr) * delta
    new_upr = fit + (upr - fit) * delta
    
    return np.column_stack((fit, new_lwr, new_upr))

# x is provided by data_shim
# d <- data.frame(y=rnorm(length(x),x),x=x)
# R's rnorm(n, mean) where mean is a vector: each element is drawn from N(mean[i], 1)
# r2py:entity:d
y = np.random.normal(loc=np.array(x), scale=1.0)
d = pd.DataFrame({'y': y, 'x': x})

# l <- lm(y~x,d)
# r2py:entity:l
X_d = sm.add_constant(d['x'])
l = sm.OLS(d['y'], X_d).fit()

# plot(y~x,d)
# r2py:entity:plot
plt.figure()
plt.scatter(d['x'], d['y'])

# abline(l)
# r2py:entity:abline
plt.plot(d['x'], l.predict(X_d), color='black')

# d0 <- data.frame(x=seq(-5,5,length.out=100))
# r2py:entity:d0
d0 = pd.DataFrame({'x': np.linspace(-5, 5, 100)})

# d1 <- cbind(d0,predict(l,newdata=d0,interval="confidence"))
# r2py:entity:d1
X0 = sm.add_constant(d0['x'], has_constant='add')
pred_obj = l.get_prediction(X0)
pred_frame = pred_obj.summary_frame(alpha=0.05)
d1 = pd.concat([d0, pred_frame[['mean', 'mean_ci_lower', 'mean_ci_upper']]], axis=1)
d1.columns = ['x', 'fit', 'lwr', 'upr']

# d2 <- cbind(d0,scheffe(l,d0))
# r2py:entity:d2
scheffe_res = scheffe(l, d0)
d2 = pd.concat([d0, pd.DataFrame(scheffe_res, columns=['fit', 'lwr', 'upr'])], axis=1)

# lines(lwr~x,d1,lty=2,col="red")
# r2py:entity:lines
plt.plot(d1['x'], d1['lwr'], color='red', linestyle='--', linewidth=1)
# lines(upr~x,d1,lty=2,col="red")
# r2py:entity:lines_1
plt.plot(d1['x'], d1['upr'], color='red', linestyle='--', linewidth=1)
# lines(lwr~x,d2,lty=2,col="blue")
# r2py:entity:lines_2
plt.plot(d2['x'], d2['lwr'], color='blue', linestyle='--', linewidth=1)
# lines(upr~x,d2,lty=2,col="blue")
# r2py:entity:lines_3
plt.plot(d2['x'], d2['upr'], color='blue', linestyle='--', linewidth=1)

plt.show()