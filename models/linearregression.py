from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from scipy import stats
from sklearn import datasets, linear_model
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor 
from features_collection import df as data


def VIF(df, columns): 
    values=sm.add_constant(df[columns]).values
    # the dataframe passed to VIF␣ ↪ must include the intercept term. We add it the same way we did before. 
    num_columns=len(columns)+1#we added intercept 
    vif=[variance_inflation_factor(values, i) for i in range(num_columns)] 
    return pd.Series(vif[1:], index=columns)
def OSR2(model, y_train, x_test,y_test):
    y_pred=model.predict(x_test) 
    SSE=np.sum((y_test-y_pred)**2) 
    SST=np.sum((y_test-np.mean(y_train))**2) 
    return 1-(SSE/SST)

#use only the important features
features =data.columns
X=data
#Split into training and testing data
training_data = data[(data['Year'] >= 2010) & (data['Year'] <= 2018)]
testing_data = data[(data['Year'] >= 2019) & (data['Year'] <= 2023)]

Y=data['#INSERT HERE THE Y VARIABLE']

#Now we want to see how the model behaves. We train the linear regression.
#We will mostly focus on the p-values, the VIF values, and R2.
X2 = sm.add_constant(X)
lrm=sm.OLS(Y, X2).fit()
print(lrm.summary())
print(VIF(training_data, features))

pd.set_option('display.max_colwidth', None) 
#Importance of each feature in the Linear Regression#
params_df = pd.DataFrame({'Parameter': lrm.params.index, 'Coefficient': lrm.params.values})
sorted_params_df = params_df.iloc[params_df['Coefficient'].abs().argsort()[::-1]]
print('Importance of each feature in Linear Classification\n',sorted_params_df)

#HERE WE SHOULD DO A LITTLE BIT OF FEATURE ENGINEERING, DELETING FEATURES THAT MIGHT HAVE
#HIGH P-VALUES OR VIF VALUES (COLINEARITY).

#ELIMINATE FEATURES AND REDO PROCESS.

plt.plot(y_test, y_pred)
plt.show()