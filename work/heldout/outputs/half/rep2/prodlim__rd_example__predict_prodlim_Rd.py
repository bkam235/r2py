# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

import numpy as np
import pandas as pd
from lifelines import KaplanMeierFitter

# r2py:entity:dat
def SimSurv(N):
    """
    Approximates the R SimSurv function which generates synthetic survival data.
    R version uses a Cox-Weibull model with X1 and X2.
    """
    np.random.seed(42)
    # X1 binomial (0 or 1)
    X1 = np.random.binomial(1, 0.5, N)
    # X2 binomial (0 or 1)
    X2 = np.random.binomial(1, 0.5, N)
    
    # simulate event times using a basic Weibull-like logic based on X1, X2
    # In R: regression X1->eventtime = 1, X2->eventtime = 1
    # lambda is the scale. We use an approximation of the scale provided (1/100)
    base_hazard = 0.01
    # The effect of X1 and X2 reduces the survival time (increasing hazard)
    hazard = base_hazard * np.exp(X1 + X2)
    
    # Generate Weibull times: T = -log(U) / hazard
    eventtime = -np.log(np.random.uniform(0, 1, N)) / hazard
    # Generate censoring times
    censtime = -np.log(np.random.uniform(0, 1, N)) / base_hazard
    
    time = np.minimum(eventtime, censtime)
    status = (eventtime <= censtime).astype(int)
    
    return pd.DataFrame({'time': time, 'status': status, 'X1': X1, 'X2': X2})

# r2py:entity:fit
class ProdlimModel:
    """
    A wrapper for lifelines KaplanMeierFitter to mimic the prodlim object 
    and the predict.prodlim behavior.
    """
    def __init__(self, formula, data):
        self.formula = formula
        self.data = data
        self.kmfs = {}
        
        # Check if formula is simple (no strata/covariates)
        # R: Hist(time, status) ~ 1
        if "~ 1" in formula:
            kmf = KaplanMeierFitter()
            kmf.fit(data['time'], event_observed=data['status'])
            self.kmfs['all'] = kmf
            self.covariate_type = 1
        else:
            # R: Hist(time, status) ~ X1 + X2 (Treating as strata/grouping)
            self.covariate_type = 2
            # Parse covariates from formula
            rhs = formula.split('~')[1].strip()
            covs = [c.strip() for c in rhs.split('+')]
            
            # Create strata groups based on combinations of covariates
            data['strata'] = data[covs].astype(str).agg(':'.join, axis=1)
            for group in data['strata'].unique():
                df_group = data[data['strata'] == group]
                kmf = KaplanMeierFitter()
                kmf.fit(df_group['time'], event_observed=df_group['status'])
                self.kmfs[group] = kmf

    def predict(self, times, newdata=None, mode='list', bytime=False):
        times = np.array(times)
        
        if self.covariate_type == 1:
            kmf = self.kmfs['all']
            # KM surv prob at specific times. 
            # lifelines survival_function_at_times handles extrapolation by keeping last value
            # but R prodlim returns NA for times beyond range.
            max_t = kmf.survival_function_.index.max()
            preds = kmf.predict(times)
            preds[times > max_t] = np.nan
            preds[times < 0] = np.nan
            
            if mode == 'matrix':
                return preds.values.reshape(1, -1)
            return preds.values
            
        else:
            # Strata logic
            if newdata is None:
                raise ValueError("newdata is required when strata are present")
            
            # Mimic R strata combination
            rhs = self.formula.split('~')[1].strip()
            covs = [c.strip() for c in rhs.split('+')]
            newdata_strata = newdata[covs].astype(str).agg(':'.join, axis=1)
            
            results = []
            for strata_val in newdata_strata:
                if strata_val in self.kmfs:
                    kmf = self.kmfs[strata_val]
                    max_t = kmf.survival_function_.index.max()
                    p = kmf.predict(times)
                    p[times > max_t] = np.nan
                    p[times < 0] = np.nan
                    results.append(p.values)
                else:
                    results.append(np.full(len(times), np.nan))
            
            res_array = np.array(results) # shape (n_obs, n_times)
            
            if mode == 'matrix':
                if bytime:
                    return res_array.T
                return res_array
            
            # For mode='list', return as dictionary (mimicking R named list)
            return {f"obs_{i+1}": res_array[i] for i in range(len(res_array))}

def prodlim(formula, data):
    return ProdlimModel(formula, data)

def predict_wrapper(fit, times, newdata=None, mode='list', bytime=False):
    return fit.predict(times, newdata=newdata, mode=mode, bytime=bytime)

# Execution
# r2py:entity:dat
dat = SimSurv(400)
# r2py:entity:fit
fit = prodlim("Hist(time, status) ~ 1", data=dat)

# predict the survival probs at selected times 
# r2py:entity:predict
print(predict_wrapper(fit, times=[3, 5, 10]))

# NA is returned when the time point is beyond the range
# r2py:entity:predict_1
print(predict_wrapper(fit, times=[-1, 0, 10, 100, 1000, 10000]))

# when there are strata, newdata is required 
# r2py:entity:mfit
mfit = prodlim("Hist(time, status) ~ X1 + X2", data=dat)
# R: dat[18:21,] is 1-based, inclusive. Python: 17:21
# r2py:entity:predict_2
newdata_subset = dat.iloc[17:21]
print(predict_wrapper(mfit, times=[-1, 0, 10, 100, 1000, 10000], newdata=newdata_subset))

# this can be requested in matrix form
# r2py:entity:predict_3
print(predict_wrapper(mfit, times=[-1, 0, 10, 100, 1000, 10000], newdata=newdata_subset, mode="matrix"))

# and even transposed
# r2py:entity:predict_4
print(predict_wrapper(mfit, times=[-1, 0, 10, 100, 1000, 10000], newdata=newdata_subset, mode="matrix", bytime=True))