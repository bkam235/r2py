# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

import pandas as pd
import numpy as np
from lifelines import KaplanMeierFitter

# r2py:entity:dat
def SimSurv(N):
    """
    Simulates survival data approximating the R SimSurv function.
    Based on the provided R source, it generates two binomial covariates 
    and survival/censoring times from Cox-Weibull distributions.
    """
    np.random.seed(42)
    X1 = np.random.binomial(1, 0.5, N)
    X2 = np.random.binomial(1, 0.5, N)
    
    # Scale 1/100 in Cox-Weibull usually means lambda_val=0.01
    # Survival time T = -log(U) / lambda
    def generate_weibull(n, scale=0.01):
        return -np.log(np.random.uniform(0, 1, n)) / scale

    eventtime = generate_weibull(N) * (1 + X1 + X2)
    censtime = generate_weibull(N)
    
    time = np.minimum(eventtime, censtime)
    status = (eventtime <= censtime).astype(int)
    
    return pd.DataFrame({'time': time, 'status': status, 'X1': X1, 'X2': X2})

# r2py:entity:fit
class ProdlimFit:
    """
    Wrapper class to mimic prodlim object and its predict method.
    """
    def __init__(self, formula, data):
        self.formula = formula
        self.data = data
        self.kmf = KaplanMeierFitter()
        
        # Handle simple formula ~1 or stratified formula ~X1+X2
        if "~1" in formula:
            self.covariate_type = 1 # Global
            self.kmf.fit(data['time'], event_observed=data['status'])
            self.surv_func = self.kmf.survival_function_
        else:
            self.covariate_type = 2 # Stratified
            self.strata_cols = [col for col in data.columns if col != 'time' and col != 'status']
            # Create strata identifiers
            self.data['strata'] = self.data[self.strata_cols].astype(str).agg(':'.join, axis=1)
            self.strata_models = {}
            for s in self.data['strata'].unique():
                subset = self.data[self.data['strata'] == s]
                kmf_s = KaplanMeierFitter()
                kmf_s.fit(subset['time'], event_observed=subset['status'])
                self.strata_models[s] = kmf_s
    
    def predict(self, times, newdata=None, mode="list", bytime=False):
        # Find survival probabilities at specified times
        # R's predict.prodlim returns NA if time is outside [0, max_time]
        
        if self.covariate_type == 1:
            # Global model
            probs = []
            max_t = self.kmf.survival_function_.index.max()
            for t in times:
                if t < 0 or t > max_t:
                    probs.append(np.nan)
                else:
                    # Interpolate or find nearest survival value
                    probs.append(self.kmf.predict(t))
            
            if mode == "matrix":
                return np.array(probs).reshape(1, -1)
            return np.array(probs)

        else:
            # Stratified model
            if newdata is None:
                raise ValueError("newdata is required for stratified models")
            
            # Map newdata to strata
            newdata_strata = newdata[self.strata_cols].astype(str).agg(':'.join, axis=1)
            
            results = []
            for s_val in newdata_strata:
                if s_val in self.strata_models:
                    kmf_s = self.strata_models[s_val]
                    max_t = kmf_s.survival_function_.index.max()
                    s_probs = []
                    for t in times:
                        if t < 0 or t > max_t:
                            s_probs.append(np.nan)
                        else:
                            s_probs.append(kmf_s.predict(t))
                    results.append(s_probs)
                else:
                    results.append([np.nan] * len(times))
            
            if mode == "matrix":
                res_mat = np.array(results)
                if bytime:
                    return res_mat.T
                return res_mat
            
            # Return as dict to mimic R list
            names = newdata_strata.tolist()
            return {name: np.array(prob) for name, prob in zip(names, results)}

def prodlim(formula, data):
    return ProdlimFit(formula, data)

# r2py:entity:predict
def predict(fit, times, newdata=None, mode="list", bytime=False):
    return fit.predict(times, newdata=newdata, mode=mode, bytime=bytime)

# --- Main execution ---

dat = SimSurv(400)
fit = prodlim("Hist(time,status)~1", data=dat)

# predict the survival probs at selected times 
print(predict(fit, times=[3, 5, 10]))

# NA is returned when the time point is beyond the range of definition
# r2py:entity:predict_1
print(predict(fit, times=[-1, 0, 10, 100, 1000, 10000]))

# when there are strata, newdata is required
# r2py:entity:mfit
mfit = prodlim("Hist(time,status)~X1+X2", data=dat)
# dat[18:21,] in R (1-based) is indices 17, 18, 19, 20 in Python (0-based slice [17:21])
# r2py:entity:predict_2
newdata_subset = dat.iloc[17:21]
print(predict(mfit, times=[-1, 0, 10, 100, 1000, 10000], newdata=newdata_subset))

# this can be requested in matrix form
# r2py:entity:predict_3
print(predict(mfit, times=[-1, 0, 10, 100, 1000, 10000], newdata=newdata_subset, mode="matrix"))

# and even transposed
# r2py:entity:predict_4
print(predict(mfit, times=[-1, 0, 10, 100, 1000, 10000], newdata=newdata_subset, mode="matrix", bytime=True))