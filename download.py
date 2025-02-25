import yfinance as yf
import numpy as np
import pandas as pd

#The M6 asset universe
assets = [
  "ABBV","ACN","AEP","AIZ","ALLE","AMAT","AMP","AMZN","AVB","AVY",
  "AXP","BDX","BF-B","BMY","BR","CARR","CDW","CE","CHTR","CNC",
  "CNP","COP","CTAS","CZR","DG","DPZ","DRE","DXC","FB","FTV",
  "GOOG","GPC","HIG","HST","JPM","KR","OGN","PG","PPL","PRU",
  "PYPL","RE","ROL","ROST","UNH","URI","V","VRSK","WRK","XOM",
  "IVV","IWM","EWU","EWG","EWL","EWQ","IEUS","EWJ","EWT","MCHI",
  "INDA","EWY","EWA","EWH","EWZ","EWC","IEMG","LQD","HYG","SHY",
  "IEF","TLT","SEGA.L","IEAA.L","HIGH.L","JPEA.L","IAU","SLV","GSG","REET",
  "ICLN","IXN","IGF","IUVL.L","IUMO.L","SPMV.L","IEVL.L","IEFM.L","MVEU.L","XLK",
  "XLF","XLV","XLE","XLY","XLI","XLC","XLU","XLP","XLB","VXX"]

#Download historical data (select starting date)
starting_date = "2015-01-01"
future_starting_date = pd.to_datetime("2022-03-06")
future_end_date = pd.to_datetime("2022-04-01")

data = yf.download(assets, start=starting_date)

forecast_horizon = pd.date_range(start=future_starting_date, end=future_end_date)
df_future = data.iloc[0:len(forecast_horizon)]
df_future.index = forecast_horizon
df_future.index.name = 'Date'
df_future = df_future.applymap(lambda x: np.nan)


data = data.stack().reset_index()
data.rename(columns={"Date": "date",
                     "level_1":"symbol",
                     "Adj Close": "price",
                     "Close":"close",
                     "High":"high",
                     "Low":"low",
                     "Open":"open",
                     "Volume":"volume"}, inplace=True)
for col in ['price', 'close', 'high', 'low', 'open']:
    data[col] = np.round(data[col].values, 2)


df_future = df_future.stack(dropna=False).reset_index()
df_future.rename(columns={"Date": "date",
                         "level_1":"symbol",
                         "Adj Close": "price",
                         "Close":"close",
                         "High":"high",
                         "Low":"low",
                         "Open":"open",
                         "Volume":"volume"}, inplace=True)

data = pd.concat([data, df_future], sort=False)
data.to_csv('full_asset_m6.csv', index=False)