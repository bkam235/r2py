# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

import pandas as pd
import numpy as np
from lifelines import KaplanMeierFitter, CoxPHFitter

# Simulation of SimSurv(400)
# SimSurv creates a dataset with time, status, and covariates X1, X2
# r2py:entity:dat
np.random.seed(42)
n = 400
X1 = np.random.normal(0, 1, n)
X2 = np.random.normal(0, 1, n)
# Simulate survival times using a Cox-like hazard (exp(X1 + X2))
hazard = np.exp(X1 + X2)
time = np.random.exponential(1 / hazard)
status = np.random.binomial(1, 0.8, n) # 80% events
dat = pd.DataFrame({'time': time, 'status': status, 'X1': X1, 'X2': X2})

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
print(kmf.predict(times2))

# mfit <- prodlim(Hist(time,status)~X1+X2,data=dat)
# Note: prodlim's linear predictor for Hist is approximated by CoxPHFitter in Python
# r2py:entity:mfit
mfit = CoxPHFitter()
mfit.fit(dat, duration_col='time', event_col='status')

# predict(mfit,times=c(-1,0,10,100,1000,10000),newdata=dat[18:21,])
# Note: Python indices are 0-based. R 18:21 corresponds to 17:21 in slice
# r2py:entity:predict_2
newdata = dat.iloc[17:21]
surv_probs = mfit.predict_survival_function(newdata, times=times2)
print(surv_probs)

# predict(mfit,times=c(-1,0,10,100,1000,10000),newdata=dat[18:21,],mode="matrix")
# The output of predict_survival_function is already a matrix/dataframe
# r2py:entity:predict_3
print(surv_probs.values)

# predict(mfit,times=c(-1,0,10,100,1000,10000),newdata=dat[18:21,],mode="matrix",bytime=TRUE)
# Transposing the survival matrix to align by time
# r2py:entity:predict_4
print(surv_probs.T)