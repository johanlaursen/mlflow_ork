import numpy as np
class Transform():
    
    def __init__(self):
        pass
        
    def fit(self,X,Y=None):
        return self
    
    def transform(self,df):
        df = df.copy()
        deg_enc= {'NNE':22.5,
     'NE':45,
     'E':90,
     'ESE':112.5,
     'SE':135,
     'SSE':157.5,
     'SW':225,
     'SSW':202.5,
     'S':180,
     'WSW':247.5,
     'W':270,
     'WNW':292.5,
     'NW':315,
     'NNW':337.5,
     'N':0,
     'ENE':67.5}
        speed = df.pop("Speed")
        df["Direction"] = df["Direction"].map(deg_enc)
        dir_rad = np.radians(df.pop("Direction"))

        df["Wx"] = speed*np.cos(dir_rad)
        df["Wy"] = speed*np.sin(dir_rad)

        X = df[["Wx","Wy"]]
        return X
