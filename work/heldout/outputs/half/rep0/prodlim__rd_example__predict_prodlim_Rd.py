# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

import pandas as pd
import numpy as np
from lifelines import KaplanMeierFitter, CoxPHFitter

# Simulating the SimSurv(400) dataset behavior
# SimSurv typically generates time, status, and some covariates X1, X2...
# r2py:entity:dat
np.random.seed(42)
n = 400
dat = pd.DataFrame({
    'time': np.random.exponential(10, n),
    'status': np.random.binomial(1, 0.8, n),
    'X1': np.random.normal(0, 1, n),
    'X2': np.random.normal(0, 1, n)
})

# fit <- prodlim(Hist(time,status)~1,data=dat)
# r2py:entity:fit
kmf = KaplanMeierFitter()
kmf.fit(dat['time'], event_observed=dat['status'])

# predict(fit,times=c(3,5,10))
# r2py:entity:predict
times1 = [3, 5, 10]
print(kmf.predict(times1))

# predict(fit,times=c(-1,0,10,100,1000,10000))
# r2py:entity:predict_1
times2 = [-1, 0, 10, 100, 1000, 10000]
# lifelines handles values outside range by clamping or extrapolating linearly based on survival
print(kmf.predict(times2))

# mfit <- prodlim(Hist(time,status)~X1+X2,data=dat)
# Note: prodlim's formula interface for covariates often maps to Cox or AFT models 
# depending on context. CoxPHFitter is the standard Python equivalent for covariate survival.
# r2py:entity:mfit
cph = CoxPHFitter()
cph.fit(dat, duration_col='time', event_col='status', formula="X1 + X2")

# predict(mfit,times=c(-1,0,10,100,1000,10000),newdata=dat[18:21,])
# r2py:entity:predict_2
newdata = dat.iloc[17:20] # R 18:21 is Python 17:20 (0-indexed, exclusive stop)
times3 = [-1, 0, 10, 100, 1000, 10000]

# To predict survival probabilities at specific times for new data:
# We calculate the survival function for each subject and sample the specific times
surv_funcs = cph.predict_survival_function(newdata, times=times3)
print(surv_funcs)

# predict(mfit,times=c(-1,0,10,100,1000,10000),newdata=dat[18:21,],mode="matrix")
# This is essentially the dataframe representation of the survival probabilities
# r2py:entity:predict_3
print(surv_funcs.values)

# predict(mfit,times=c(-1,0,10,100,1000,10000),newdata=dat[18:21,],mode="matrix",bytime=TRUE)
# This is equivalent to the survival function dataframe where columns are times
# r2py:entity:predict_4
print(surv_funcs)