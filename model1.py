import numpy as np
import pandas as pd

from xgboost import XGBRegressor, cv, plot_importance
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import accuracy_score

stat_data = pd.read_csv('data/summarised/base_stats.csv')
stat_data = stat_data.dropna() # NAs from lag shift

features = [col for col in stat_data.columns if col.startswith('prev')]
X = stat_data[features]
X.drop('prev_position', axis=1, inplace=True)
y = stat_data['fantasy_points']
X.columns

model_params = {
    "tree_method": "hist",
    "seed": 1234,
    "n_estimators": 1000,
    "max_depth": 7,
    "eta": 0.1,
    "subsample": 0.7,
    "colsample_bytree": 0.8,
    "enable_categorical": True
}

model = XGBRegressor(**model_params)
accuracies=cross_val_score(estimator=model,
                           X=X,
                           y=y,
                           cv=8,
                           n_jobs=-1,
                           scoring='neg_root_mean_squared_error')
# >>> accuracies
# array([-17.58909675, -17.22713347, -17.78423831, -18.14432617,
#        -17.76850477, -17.22250843, -17.85063924, -17.49863127])

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3, random_state=1234)

model = XGBRegressor(**model_params)
model.fit(X_train, y_train)

import matplotlib.pylab as plt
from matplotlib import pyplot
from xgboost import plot_importance
ax = plot_importance(model, max_num_features=20) # top 10 most important features
ax.figure.tight_layout()
ax.figure.savefig('plots/basic_importance.png')

