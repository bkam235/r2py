# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

import numpy as np
import pandas as pd
from lifelines import KaplanMeierFitter

# r2py:entity:dat
def SimSurv(N):
    """
    Simulates survival data mimicking the provided R SimSurv logic.
    The R version uses coxWeibull distributions for event and censoring times.
    """
    np.random.seed(42)
    # Scale = 1/100 in R coxWeibull often corresponds to lambda_val= 100 
    # or a characteristic life. Here we approximate the behavior.
    # eventtime and censtime follow Weibull(shape=1, scale=100) -> Exponential(1/100)
    eventtime = np.random.exponential(100, N)
    censtime = np.random.exponential(100, N)
    
    # time = min(eventtime, censtime), status = 1 if eventtime <= censtime
    time = np.minimum(eventtime, censtime)
    status = (eventtime <= censtime).astype(int)
    
    # X1 and X2 are binomial (simulated as Bernoulli)
    X1 = np.random.binomial(1, 0.5, N)
    X2 = np.random.binomial(1, 0.5, N)
    
    return pd.DataFrame({'time': time, 'status': status, 'X1': X1, 'X2': X2})

# r2py:entity:fit
class ProdlimModel:
    """
    A wrapper for lifelines KaplanMeierFitter to mimic the prodlim predict API.
    """
    def __init__(self, formula, data):
        self.formula = formula
        self.data = data
        self.kmf = KaplanMeierFitter()
        
        # Parse formula: Hist(time, status) ~ 1 or Hist(time, status) ~ X1 + X2
        # Right side of formula determines strata
        rhs = formula.split('~')[1].strip()
        
        if rhs == '1':
            self.covariate_type = 1 # No covariates
            self.kmf.fit(data['time'], event_observed=data['status'])
            self.strata_cols = []
        else:
            self.covariate_type = 2 # Strata present
            self.strata_cols = [x.strip() for x in rhs.split('+')]
            # In R, prodlim with formula ~ X1 + X2 creates strata for every unique combination
            self.strata_models = {}
            # Create a strata identifier
            self.data['_strata'] = self.data[self.strata_cols].astype(str).agg(':'.join, axis=1)
            for strata_val, group in self.data.groupby('_strata'):
                kmf_s = KaplanMeierFitter()
                kmf_s.fit(group['time'], event_observed=group['status'])
                self.strata_models[strata_val] = kmf_s

    def predict(self, times, newdata=None, mode="list", bytime=False):
        # Handle times beyond range: R's prodlim returns NA
        # lifelines .predict() handles this via extrapolation or clipping, 
        # we manually check boundaries to match R's NA behavior.
        
        if self.covariate_type == 1:
            # Single survival curve
            max_t = self.kmf.survival_function_.index.max()
            min_t = 0 # KM starts at 0
            
            surv_probs = []
            for t in times:
                if t < min_t or t > max_t:
                    surv_probs.append(np.nan)
                else:
                    # Get survival probability at time t
                    surv_probs.append(self.kmf.predict(t))
            
            result = np.array(surv_probs)
            if mode == "matrix":
                return result.reshape(1, -1)
            return result

        else:
            # Stratified survival curves
            if newdata is None:
                raise ValueError("newdata is required when strata are present")
            
            # Identify strata for newdata
            newdata_strata = newdata[self.strata_cols].astype(str).agg(':'.join, axis=1)
            
            all_preds = []
            for s_val in newdata_strata:
                if s_val not in self.strata_models:
                    # If strata not found in training, return NaNs
                    all_preds.append([np.nan] * len(times))
                    continue
                
                kmf_s = self.strata_models[s_val]
                max_t = kmf_s.survival_function_.index.max()
                
                s_probs = []
                for t in times:
                    if t < 0 or t > max_t:
                        s_probs.append(np.nan)
                    else:
                        s_probs.append(kmf_s.predict(t))
                all_preds.append(s_probs)
            
            res_array = np.array(all_preds) # Shape: (n_newdata, n_times)
            
            if mode == "matrix":
                if bytime:
                    return res_array.T # Transposed: times as rows, strata as cols
                return res_array
            
            # Default mode "list" (return as dict/list of arrays)
            return {idx: res_array[idx] for idx in range(len(all_preds))}

def prodlim(formula, data):
    return ProdlimModel(formula, data)

# r2py:entity:predict
def predict(object_fit, times, newdata=None, mode="list", bytime=False):
    return object_fit.predict(times, newdata=newdata, mode=mode, bytime=bytime)

# --- Execution ---

# r2py:entity:dat
dat = SimSurv(400)
# r2py:entity:fit
fit = prodlim("Hist(time, status) ~ 1", data=dat)

# predict the survival probs at selected times 
# r2py:entity:predict
print(predict(fit, times=[3, 5, 10]))

# NA is returned when the time point is beyond the range
# r2py:entity:predict_1
print(predict(fit, times=[-1, 0, 10, 100, 1000, 10000]))

# when there are strata, newdata is required 
# r2py:entity:mfit
mfit = prodlim("Hist(time, status) ~ X1 + X2", data=dat)
# R index 18:21 is 17 to 21 (exclusive) in Python
# r2py:entity:predict_2
dat_subset = dat.iloc[17:21] 
print(predict(mfit, times=[-1, 0, 10, 100, 1000, 10000], newdata=dat_subset))

# this can be requested in matrix form
# r2py:entity:predict_3
print(predict(mfit, times=[-1, 0, 10, 100, 1000, 10000], newdata=dat_subset, mode="matrix"))

# and even transposed
# r2py:entity:predict_4
print(predict(mfit, times=[-1, 0, 10, 100, 1000, 10000], newdata=dat_subset, mode="matrix", bytime=True))