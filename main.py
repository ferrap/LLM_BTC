import pandas as pd
import requests

df = pd.DataFrame()
URL = 'https://min-api.cryptocompare.com/data/histoday?fsym=ETH&tsym=USD&allData=true' 
res = requests.get(URL)
res_json = res.json()
data= res_json['Data']
temp_df= pd.DataFrame(data)
temp_df['conversionSymbol']= 'USD'
df = df.concat(temp_df, ignore_index=True)
df['time']=pd.to_datetime(df['time'],unit='s')
df['time'] = df['time'].dt.strftime('%d/%m/%Y')
