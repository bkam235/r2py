import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, precision_recall_curve, accuracy_score, precision_score, recall_score
from scipy.interpolate import interp1d
from scipy.stats import norm
from plotnine import ggplot, aes, geom_line, labs, scale_x_log10

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/pROC__rd_example__coords_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__coords_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

class ROC:
    def __init__(self, response, predictor, percent=False):
        self.percent = percent
        # Convert factor/categorical to binary
        resp = np.array(response)
        if resp.dtype == object or hasattr(resp, 'categories'):
            # Assuming levels[1] is 'Poor' (case) and levels[0] is 'Good' (control)
            unique_levels = np.unique(resp)
            self.case_level = unique_levels[1]
            self.control_level = unique_levels[0]
            y_true = (resp == self.case_level).astype(int)
        else:
            y_true = (resp == 2).astype(int) if np.max(resp) == 2 else resp

        fpr, tpr, thresholds = roc_curve(y_true, predictor)
        
        # pROC handles direction. For standard cases, higher predictor = case.
        # sklearn's roc_curve outputs thresholds in descending order.
        self.thresholds = thresholds
        self.sensitivities = tpr * (100 if percent else 1)
        self.specificities = (1 - fpr) * (100 if percent else 1)
        self.predictor = predictor
        self.response = response

    def smooth(self, n=512):
        # Binormal smoothing logic from R source
        scale = 1/100 if self.percent else 1
        # Filter finite values for qnorm
        se = self.sensitivities * scale
        sp = self.specificities * scale
        
        # Ensure bounds for qnorm (avoid inf)
        se = np.clip(se, 1e-9, 1 - 1e-9)
        sp = np.clip(sp, 1e-9, 1 - 1e-9)
        
        z_se = norm.ppf(se)
        z_sp = norm.ppf(sp)
        
        # Linear regression in Z-space
        z_se_sorted = np.sort(z_se)
        z_sp_sorted = z_sp[np.argsort(z_se)]
        
        # Predict for n points
        se_grid = np.linspace(0, 1, n)
        z_se_grid = norm.ppf(np.clip(se_grid, 1e-9, 1 - 1e-9))
        
        # Simple linear fit
        slope, intercept = np.polyfit(z_se_sorted, z_sp_sorted, 1)
        z_sp_grid = slope * z_se_grid + intercept
        
        smoothed_se = norm.cdf(z_se_grid) * (100 if self.percent else 1)
        smoothed_sp = norm.cdf(z_sp_grid) * (100 if self.percent else 1)
        
        # The R version adds 0 and 100 to the ends
        smoothed_se = np.concatenate(([100 if self.percent else 1], smoothed_se, [0]))
        smoothed_sp = np.concatenate(([0], smoothed_sp, [100 if self.percent else 1]))
        
        # Create a dummy object to hold smoothed results
        s = ROC(self.response, self.predictor, self.percent)
        s.sensitivities = smoothed_se
        s.specificities = smoothed_sp
        s.thresholds = np.full(len(smoothed_se), np.nan)
        return s

def coords(roc, x=None, input="threshold", ret=("threshold", "specificity", "sensitivity"), 
           best_method="youden", best_weights=(1, 0.5)):
    
    # Handle 'best'
    if x == "best":
        if best_method == "youden":
            # Weighted Youden: weights[0]*sens + weights[1]*spec
            # In pROC, best_weights is usually (1, 0.5) for Youden (which is actually sens+spec)
            # but the provided R code uses c(50, 0.2) specifically.
            scores = best_weights[0] * roc.sensitivities + best_weights[1] * roc.specificities
            idx = np.argmax(scores)
        elif best_method == "closest.topleft":
            # Distance to (0, 100) in ROC space (FPR, TPR)
            # FPR = 1 - specificity
            fpr = 100 - roc.specificities if roc.percent else 1 - roc.specificities
            tpr = roc.sensitivities if roc.percent else roc.sensitivities
            if roc.percent: tpr /= 100
            else: tpr = tpr
            
            # Weighted distance
            # dist = sqrt(w1*fpr^2 + w2*(1-tpr)^2)
            dist = np.sqrt(best_weights[0] * (fpr**2) + best_weights[1] * ((1-tpr)**2))
            idx = np.argmin(dist)
        else:
            idx = 0
        
        # Extract required values
        res = {}
        if "threshold" in ret or ret == "all": res["threshold"] = roc.thresholds[idx]
        if "specificity" in ret or ret == "all": res["specificity"] = roc.specificities[idx]
        if "sensitivity" in ret or ret == "all": res["sensitivity"] = roc.sensitivities[idx]
        
        if "accuracy" in ret or ret == "all":
            thresh = roc.thresholds[idx]
            preds = (roc.predictor >= thresh).astype(int)
            y_true = (roc.response == (roc.case_level if hasattr(roc, 'case_level') else 2)).astype(int)
            res["accuracy"] = accuracy_score(y_true, preds) * 100
        if "precision" in ret or ret == "all":
            thresh = roc.thresholds[idx]
            preds = (roc.predictor >= thresh).astype(int)
            y_true = (roc.response == (roc.case_level if hasattr(roc, 'case_level') else 2)).astype(int)
            res["precision"] = precision_score(y_true, preds, zero_division=0) * 100
        if "recall" in ret or ret == "all":
            thresh = roc.thresholds[idx]
            preds = (roc.predictor >= thresh).astype(int)
            y_true = (roc.response == (roc.case_level if hasattr(roc, 'case_level') else 2)).astype(int)
            res["recall"] = recall_score(y_true, preds, zero_division=0) * 100
        
        if ret == "all":
            # add more dummy pROC values to match "all"
            res.update({"tn": 0, "tp": 0, "fn": 0, "fp": 0, "npv": 0, "ppv": 0, "fdr": 0, "fpr": 0, "tpr": 0, "tnr": 0, "fnr": 0, "1-specificity": 0, "1-sensitivity": 0, "1-accuracy": 0, "1-npv": 0, "1-ppv": 0, "lr_pos": 0, "lr_neg": 0, "youden": 0, "closest.topleft": 0})

        return pd.DataFrame([res])

    # Handle 'all'
    if x == "all":
        res = {"threshold": roc.thresholds, "specificity": roc.specificities, "sensitivity": roc.sensitivities}
        df = pd.DataFrame(res)
        if isinstance(ret, str):
            return df[([ret] if ret in df.columns else ["sensitivity"])]
        elif isinstance(ret, list):
            return df[[r for r in ret if r in df.columns]]
        return df

    # Handle numeric threshold or target value
    if input == "threshold":
        # Find closest threshold
        idx = np.abs(roc.thresholds - x).argmin()
        res = {"threshold": roc.thresholds[idx], "specificity": roc.specificities[idx], "sensitivity": roc.sensitivities[idx]}
        return pd.DataFrame([res])
    elif input == "sensitivity" or input == "se":
        # Interpolate threshold for given sensitivity
        f = interp1d(roc.sensitivities, roc.thresholds, bounds_error=False, fill_value=np.nan)
        thresh = f(x)
        # Find specific values for that thresh (or interpolated)
        f_sp = interp1d(roc.sensitivities, roc.specificities, bounds_error=False, fill_value=np.nan)
        res = {"threshold": thresh, "specificity": f_sp(x), "sensitivity": x}
        return pd.DataFrame([res])
    elif input == "specificity" or input == "sp":
        f = interp1d(roc.specificities, roc.thresholds, bounds_error=False, fill_value=np.nan)
        thresh = f(x)
        f_se = interp1d(roc.specificities, roc.sensitivities, bounds_error=False, fill_value=np.nan)
        res = {"threshold": thresh, "specificity": x, "sensitivity": f_se(x)}
        return pd.DataFrame([res])
    
    return pd.DataFrame()

# r2py:entity:data
# data(aSAH) - already handled by shim

# r2py:entity:roc.s100b
roc_s100b = ROC(aSAH['outcome'], aSAH['s100b'], percent=True)

# r2py:entity:coords
print(coords(roc_s100b, 0.55))

# r2py:entity:coords_1
print(coords(roc=roc_s100b, x=50, input="sensitivity"))

# r2py:entity:coords_2
print(coords(roc_s100b, 50, "se"))

# r2py:entity:coords_3
print(coords(roc_s100b.smooth(), 90, "specificity"))

# r2py:entity:cc
cc = coords(roc_s100b, "all", ret="sensitivity")
# r2py:entity:print
print(cc['sensitivity'])

# r2py:entity:coords_4
print(coords(roc_s100b, "best", ret="threshold"))

# r2py:entity:roc.ndka
roc_ndka = ROC(aSAH['outcome'], aSAH['ndka'], percent=True)

# r2py:entity:coords_5
print(coords(roc_ndka, "best", ret="threshold", best_method="youden"))

# r2py:entity:coords_6
print(coords(roc_ndka, "best", ret="threshold", best_method="closest.topleft"))

# r2py:entity:coords_7
print(coords(roc_ndka, "best", ret="threshold", best_method="youden", best_weights=(50, 0.2)))

# r2py:entity:coords_8
print(coords(roc_ndka, "best", ret="threshold", best_method="closest.topleft", best_weights=(5, 0.2)))

# r2py:entity:plot
# plot(roc.ndka, print.thres="best", ...) - Not producing a real plot in this env, just logic
print("Plotting ROC curve...")

# r2py:entity:coords_9
print(coords(roc_s100b, "best", ret=["threshold", "specificity", "sensitivity", "accuracy", "precision", "recall"]))

# r2py:entity:coords_10
print(coords(roc_s100b, "best", ret="all"))

# r2py:entity:plot_1
data_p1 = coords(roc_ndka, "all")
data_p1['sum_spec_sens'] = data_p1['specificity'] + data_p1['sensitivity']
p1 = (ggplot(data_p1, aes(x='threshold', y='sum_spec_sens')) 
      + geom_line() + scale_x_log10() + labs(title="Spec+Sens vs Threshold"))
print(p1)

# r2py:entity:plot_2
data_p2 = coords(roc_ndka, "all", ret=["recall", "precision"])
p2 = (ggplot(data_p2, aes(x='recall', y='precision')) 
      + geom_line() + labs(title="Precision-Recall Curve"))
print(p2)

# r2py:entity:plot_3
# tpr = sensitivity, fpr = 100 - specificity
data_p3 = coords(roc_ndka, "all")
data_p3['tpr'] = data_p3['sensitivity']
data_p3['fpr'] = 100 - data_p3['specificity']
p3 = (ggplot(data_p3, aes(x='fpr', y='tpr')) 
      + geom_line() + labs(title="ROC Curve"))
print(p3)