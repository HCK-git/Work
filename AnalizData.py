import pandas as pd
from pprint import pprint
import numpy as np

df = pd.read_csv('Data', encoding='1251')

pd.set_option('display.max_columns', None)
# print(df)

EMITENT_FULL_NAME = df['EMITENT_FULL_NAME']
DISCLOSURE_RF_INFO_PAGE = df['DISCLOSURE_RF_INFO_PAGE']

data = {'EMITENT_FULL_NAME': EMITENT_FULL_NAME, 'DISCLOSURE_RF_INFO_PAGE': DISCLOSURE_RF_INFO_PAGE}
inform_df = pd.DataFrame(data)
print(inform_df)

inform_dict = inform_df.set_index('EMITENT_FULL_NAME').T.to_dict('list')
pprint(inform_dict)