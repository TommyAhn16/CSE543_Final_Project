# key = "WUJ3DLML0IG4WL6W"
key = "6KC4LXT70B7P9KRY"

def makeurl(keyword, stock, key=key):
    url = f"https://www.alphavantage.co/query?function={keyword}&symbol={stock}&apikey={key}"
    return url

def makeFactorName(keyword, interval, time_period):
    return f"{keyword}_{interval}_{time_period}"

def makeurlMA(keyword, stock, interval, time_period, series_type="close", key=key):
    url = f"https://www.alphavantage.co/query?function={keyword}&symbol={stock}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={key}"
    return url

def makeurlHT(keyword, stock, interval, series_type="close", key=key):
    url = f"https://www.alphavantage.co/query?function={keyword}&symbol={stock}&interval={interval}&series_type={series_type}&apikey={key}"
    return url

class MAfactor():
    def __init__(self, factorname, timeperiod):
        self.name = factorname
        self.timeperiod = timeperiod


abc = 1

import datetime

def getDate(date0, tdays):
    '''time0: string
    tdays: number of days    int
    return: tdays before date0
    '''
    b =datetime.datetime.strptime(date0,"%Y-%m-%d")
    return str(b-datetime.timedelta(days=tdays))



import requests
import pandas as pd

def getFactor(url, factor, dateList):
    factorName = makeFactorName(keyword=factor.name, interval="daily", time_period=factor.timeperiod)
      
    r = requests.get(url)
    data = r.json()
    if data and len(data[f"Technical Analysis: {factor.name}"]):
        df = pd.DataFrame(data[f"Technical Analysis: {factor.name}"]).T[factor.name]
        df = df.reindex(dateList)
        df = df.fillna(value=0)
        df.name = factorName
        return pd.DataFrame(df)
    else:
        return pd.DataFrame(index=dateList)


import numpy as np
def Symmetric_Orthogonalize(DF):
    F = DF.values
    M = np.dot(F.T, F)
    D, U = np.linalg.eig(M)
    D = D ** (-0.5)
    if np.sum(np.isnan(D)) != 0:
        # logging.error(" eigen values too small, Nan in D, Date："+str(DF.iloc[0].name[0]))
        print(DF.index.get_level_values(0)[0])
        return DF
    D = np.diag(D)
    S = np.dot(np.dot(U, D), U.T)
    F = np.dot(F, S)
    DF = pd.DataFrame(F, index=DF.index, columns=DF.columns)
    return DF