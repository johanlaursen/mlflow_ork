import mlflow.tracking
import mlflow.pyfunc
import mlflow
from custom_transformer import Transform
from prepros import get_train_test
import sys
import numpy
import pandas
import influxdb


# Custom Transform class to convert wind direction and speed to combined X and Y direction/speed vector

####################################################
## Preprocess the data / Compose your pipeline

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression as LR
from sklearn.preprocessing import PolynomialFeatures as PF
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit as TSS
import pickle
from sklearn.model_selection import GridSearchCV

# Get data
#X_train, Y_train, X_test, Y_test = get_train_test(split=1.0, days=30)
X,Y = get_train_test(days=120)

#mlflow.set_tracking_uri('sqlite:///mlflow.db')
mlflow.sklearn.autolog()
try:
    mlflow.set_experiment(f"{sys.argv[1]}")
except:
    mlflow.set_experiment("Default")


poly_params = {'Poly__degree': range(1,7),}



with mlflow.start_run():
    pipeline = Pipeline([
        ("transform",Transform()),
        ('scaler', StandardScaler()),
        ("Poly", PF()), 
        ("regression", LR())
    ])

        
    
    grid = GridSearchCV(pipeline,poly_params,scoring="r2",cv=TSS())
    grid.fit(X,Y)
# plt.clf()
# plotting_x = np.linspace(min)


####################################################
## Do forecasting with the best one

# Get all future forecasts regardless of lead time
#forecasts  = client.query(
#    "SELECT * FROM MetForecasts where time > now()"
#    ) # Query written in InfluxQL
#for_df = get_df(forecasts)
#
## Limit to only the newest source time
#newest_source_time = for_df["Source_time"].max()
#newest_forecasts = for_df.loc[for_df["Source_time"] == newest_source_time].copy();
#
#del newest_forecasts["Lead_hours"]
#del newest_forecasts["Source_time"]
#
#
## Preprocess the forecasts and do predictions in one fell swoop 
## using your best pipeline.
#print("\nPredicting with best model:\n")
#print(best_model.predict(newest_forecasts))
