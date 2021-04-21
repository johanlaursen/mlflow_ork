from influxdb import InfluxDBClient # install via " pip install influxdb "
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split as TTS

def get_train_test(split=0.7,days=30):

    client = InfluxDBClient(host='influxus.itu.dk', port=8086, username='lsda', password='icanonlyread')
    client.switch_database('orkney')

    def get_df(results):
        values = results.raw["series"][0]["values"]
        columns = results.raw["series"][0]["columns"]
        df = pd.DataFrame(values, columns=columns).set_index("time")
        df.index = pd.to_datetime(df.index) # Convert to datetime-index
        return df


    # Get the last 90 days of power generation data
    generation = client.query(
        f"SELECT * FROM Generation where time > now()-{days}d"
        ) # Query written in InfluxQL

    # Get the last 90 days of weather forecasts with the shortest lead time
    wind  = client.query(
        f"SELECT * FROM MetForecasts where time > now()-{days}d and time <= now() and Lead_hours = '1'"
        ) # Query written in InfluxQL


    gen_df = get_df(generation)
    wind_df = get_df(wind)

    # Align the data frames
    df = pd.merge(gen_df.copy(),wind_df.copy(),left_index=True,right_index=True)
    X = df[["Direction","Speed"]]
    Y = df[["Total","ANM"]]
    del Y["ANM"] # please ignore this
    
    #train_x, test_x = TTS(X,train_size=split,shuffle=False)
    #train_y, test_y = TTS(Y,train_size=split,shuffle=False)
    #return train_x, train_y, test_x, test_y
    return X,Y
