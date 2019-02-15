import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from WeatherStationData import DataFeatures, FetchandStore
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

X, y = DataFeatures.find_relation(FetchandStore.sensors)
X = np.array(X)
y = np.array(y)
X = X.reshape(X.shape[0], 1)
y = y.reshape(y.shape[0], 1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

regressor = LinearRegression()
regressor.fit(X_train, y_train)
y_pred = regressor.predict(y_test)

# plt.scatter(X_train, y_train, color = 'r')
plt.scatter(X_test, y_test, color='r', marker='*')
plt.plot(X_train, regressor.predict(X_train), color='b')
plt.show()