from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from scipy import stats
from sklearn import datasets, linear_model
import statsmodels.api as sm
from features_collection import df as data

#DEFINE Y and divide between train and test#


logistic_regression = LogisticRegression()
logistic_classification = logistic_regression.fit()
threshold = 0.5 #try different thresholds and see how the model behaves
k=logistic_classification.predict(test_data)
predictions_logistic_classification = (logistic_classification.predict(test_data)>=threshold).astype(int).to_list()
params_df = pd.DataFrame({'Parameter': logistic_classification.params.index, 'Coefficient': logistic_classification.params.values})
sorted_params_df = params_df.iloc[params_df['Coefficient'].abs().argsort()[::-1]]
print('Importance of each feature in Logistic Classification\n',sorted_params_df)

# Display the model summary
print(logistic_classification.summary())
logistic_accuracy = accuracy_score(y_test, predictions_logistic_classification)
logistic_conf_matrix = confusion_matrix(y_test, predictions_logistic_classification)
logistic_tpr = logistic_conf_matrix[1, 1] / (logistic_conf_matrix[1, 0] + logistic_conf_matrix[1, 1])
logistic_fpr = logistic_conf_matrix[0, 1] / (logistic_conf_matrix[0, 0] + logistic_conf_matrix[0, 1])

plt.plot(y_test, model.predict(x_test))
plt.show()