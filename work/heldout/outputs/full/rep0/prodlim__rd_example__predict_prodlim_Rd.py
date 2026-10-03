# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

import pandas as pd
import numpy as np
from lifelines import KaplanMeierFitter

# r2py:entity:dat
def SimSurv(N):
    """
    Simulate survival data based on the logic provided in the R SimSurv/survModel.
    It generates X1, X2 as binomials and event/censoring times as Weibull.
    """
    np.random.seed(42)
    X1 = np.random.binomial(1, 0.5, N)
    X2 = np.random.binomial(1, 0.5, N)
    
    # In R: regression(m, from_val="X1", to="eventtime") <- 1
    # eventtime ~ X1 + X2. Scale 1/100 approx lambda_val= 0.01
    # Simplified simulation matching the intent:
    def gen_weibull(beta):
        # scale = 1/100 in R coxWeibull usually means lambda_val=0.01
        return np.random.weibull(1) / 0.01 * np.exp(-beta)

    # Approximate the regression effect on the scale
    eventtime = gen_weibull(X1 + X2)
    censtime = gen_weibull(0)
    
    time = np.minimum(eventtime, censtime)
    status = (eventtime <= censtime).astype(int)
    
    return pd.DataFrame({'time': time, 'status': status, 'X1': X1, 'X2': X2})

# r2py:entity:fit
class ProdlimWrapper:
    """
    Wraps lifelines KaplanMeierFitter to emulate the prodlim object and its predict method.
    """
    def __init__(self, formula, data):
        self.formula = formula
        self.data = data
        self.kmf = KaplanMeierFitter()
        
        if "~1" in formula:
            # Global fit
            self.strata_cols = []
            self.kmf.fit(data['time'], event_observed=data['status'])
        else:
            # Stratified fit
            # Formula "Hist(time,status)~X1+X2" -> strata are combinations of X1, X2
            rhs = formula.split('~')[1].strip()
            self.strata_cols = [x.strip() for x in rhs.split('+')]
            # We store models for each stratum
            self.strata_models = {}
            self.data['stratum'] = self.data[self.strata_cols].astype(str).agg(':'.join, axis=1)
            for name, group in self.data.groupby('stratum'):
                kmf_s = KaplanMeierFitter()
                kmf_s.fit(group['time'], event_observed=group['status'])
                self.strata_models[name] = kmf_s

    def predict(self, times, newdata=None, mode="list", bytime=False):
        # Handle out of range times
        def get_surv(kmf, t):
            if t < 0: return np.nan
            # lifelines survival_function_at_times handles extrapolation/bounds
            # but we want to emulate R prodlim which returns NA beyond range
            if t > kmf.survival_function_.index.max(): return np.nan
            return kmf.predict(t)

        if not self.strata_cols:
            # Single model
            results = np.array([get_surv(self.kmf, t) for t in times])
            if mode == "matrix":
                return results.reshape(1, -1)
            return results
        else:
            # Stratified models
            if newdata is None:
                raise ValueError("newdata is required for stratified models")
            
            # Determine strata for newdata
            newdata_strata = newdata[self.strata_cols].astype(str).agg(':'.join, axis=1)
            
            all_preds = []
            for s in newdata_strata:
                if s in self.strata_models:
                    kmf_s = self.strata_models[s]
                    preds = np.array([get_surv(kmf_s, t) for t in times])
                else:
                    preds = np.array([np.nan] * len(times))
                all_preds.append(preds)
            
            all_preds = np.array(all_preds) # Shape: (n_newdata, n_times)
            
            if mode == "matrix":
                if bytime:
                    return all_preds.T
                return all_preds
            
            # "list" mode in R returns a list of arrays per stratum
            return {f"stratum_{i}": all_preds[i] for i in range(len(all_preds))}

# Execute the script
dat = SimSurv(400)
fit = ProdlimWrapper("Hist(time,status)~1", data=dat)

## predict the survival probs at selected times 
# r2py:entity:predict
print(fit.predict(times=[3, 5, 10]))

## NA is returned when the time point is beyond the range
# r2py:entity:predict_1
print(fit.predict(times=[-1, 0, 10, 100, 1000, 10000]))

## when there are strata, newdata is required
# r2py:entity:mfit
mfit = ProdlimWrapper("Hist(time,status)~X1+X2", data=dat)
# R indexing dat[18:21,] is indices 17, 18, 19, 20 (0-based)
# r2py:entity:predict_2
newdata_subset = dat.iloc[17:21] 
print(mfit.predict(times=[-1, 0, 10, 100, 1000, 10000], newdata=newdata_subset))

## this can be requested in matrix form
# r2py:entity:predict_3
print(mfit.predict(times=[-1, 0, 10, 100, 1000, 10000], newdata=newdata_subset, mode="matrix"))

## and even transposed
# r2py:entity:predict_4
print(mfit.predict(times=[-1, 0, 10, 100, 1000, 10000], newdata=newdata_subset, mode="matrix", bytime=True))