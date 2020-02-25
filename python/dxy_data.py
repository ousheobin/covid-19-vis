import pandas as pd
from os import path

base_path = './DXY-COVID-19-Data/csv/'

dxy_area = pd.read_csv(path.join(base_path,'DXYArea.csv'))
dxy_area['updateTime'] = pd.to_datetime(dxy_area.updateTime).dt.date
dxy_area = dxy_area.drop_duplicates(['provinceName','updateTime']).reset_index(drop=True)
dxy_area = dxy_area[['provinceName','province_confirmedCount','province_curedCount','province_deadCount','updateTime']]
dxy_area.reset_index().to_csv('./public/data/timeseries.data.csv',index=False)
