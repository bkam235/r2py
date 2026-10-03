import pandas as pd
import numpy as np
from sklearn.svm import SVC, SVR, OneClassSVM
import matplotlib.pyplot as plt

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/e1071__rd_example__predict_svm_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'e1071__rd_example__predict_svm_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# Ensure iris is a DataFrame
# r2py:entity:data
iris = pd.DataFrame(iris)

## classification mode
# default with factor response:
# model <- svm(Species ~ ., data = iris)
# r2py:entity:model
x_model = iris.drop(columns=['Species'])
y_model = iris['Species']
model = SVC(kernel='rbf', probability=True)
model.fit(x_model, y_model)

# alternatively the traditional interface:
# x <- subset(iris, select = -Species)
# r2py:entity:x
x = iris.drop(columns=['Species'])
# y <- Species
# r2py:entity:y
y = iris['Species']
# model <- svm(x, y, probability = TRUE) 
# r2py:entity:model_1
model = SVC(kernel='rbf', probability=True)
model.fit(x, y)

# r2py:entity:print
print(model)
# summary(model) - Approximation of e1071 summary output
# r2py:entity:summary
print(f"Parameters:\n   SVM-Type:  C-classification\n SVM-Kernel:  radial\n       cost:  1\n\nNumber of Support Vectors:  {len(model.support_)}")

# test with train data
# pred <- predict(model, x)
# r2py:entity:pred
pred = model.predict(x)
# (same as:)
# pred <- fitted(model)
# r2py:entity:pred_1
pred_fitted = model.predict(x)

# compute decision values and probabilites
# pred <- predict(model, x, decision.values = TRUE, probability = TRUE)
# r2py:entity:pred_2
decision_values = model.decision_function(x)
probabilities = model.predict_proba(x)

# attr(pred, "decision.values")[1:4,]
# r2py:entity:attr
print(decision_values[0:4])
# attr(pred, "probabilities")[1:4,]
# r2py:entity:attr_1
print(probabilities[0:4])

## try regression mode on two dimensions

# create data
# x <- seq(0.1, 5, by = 0.05)
# r2py:entity:x_1
x_reg = np.arange(0.1, 5.05, 0.05)
# y <- log(x) + rnorm(x, sd = 0.2)
# Set seed for reproducibility of rnorm approximation
# r2py:entity:rnorm
np.random.seed(42)
# r2py:entity:y_1
y_reg = np.log(x_reg) + np.random.normal(0, 0.2, size=len(x_reg))

# estimate model and predict input values
# m <- svm(x, y)
# r2py:entity:m
m = SVR(kernel='rbf', C=1.0)
m.fit(x_reg.reshape(-1, 1), y_reg)
# new <- predict(m, x)
# r2py:entity:new
new = m.predict(x_reg.reshape(-1, 1))

# visualize
plt.figure()
# r2py:entity:plot
plt.plot(x_reg, y_reg, 'o', color='black', markersize=2)
# r2py:entity:points
plt.plot(x_reg, np.log(x_reg), color='red')
# r2py:entity:points_1
plt.plot(x_reg, new, color='blue')
plt.savefig('plot1.png') # To ensure graphics are captured if needed

## density-estimation

# create 2-dim. normal with rho=0:
# X <- data.frame(a = rnorm(1000), b = rnorm(1000))
# r2py:entity:X
np.random.seed(42)
X = pd.DataFrame({'a': np.random.normal(0, 1, 1000), 'b': np.random.normal(0, 1, 1000)})

# traditional way:
# m <- svm(X, gamma = 0.1)
# r2py:entity:m_2
m_density = OneClassSVM(kernel='rbf', gamma=0.1)
m_density.fit(X)

# formula interface:
# m <- svm(~., data = X, gamma = 0.1)
# m <- svm(~ a + b, gamma = 0.1)
# (Same as above)

# test:
# newdata <- data.frame(a = c(0, 4), b = c(0, 4))
# r2py:entity:newdata
newdata = pd.DataFrame({'a': [0, 4], 'b': [0, 4]})
# predict (m, newdata) - returns decision values in R for density estimation
# r2py:entity:predict
predict_dens = m_density.decision_function(newdata)
print(predict_dens)

# visualize:
# plot(X, col = 1:1000 %in% m$index + 1, xlim = c(-5,5), ylim=c(-5,5))
# r2py:entity:plot_1
plt.figure()
# support_ contains indices of support vectors
colors = np.ones(1000)
colors[m_density.support_] = 2
plt.scatter(X['a'], X['b'], c=colors, s=10, cmap='bwr')
plt.xlim(-5, 5)
plt.ylim(-5, 5)
# points(newdata, pch = "+", col = 2, cex = 5)
# r2py:entity:points_2
plt.scatter(newdata['a'], newdata['b'], marker='+', color='red', s=100)
plt.savefig('plot2.png')