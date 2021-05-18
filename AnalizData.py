import pandas as pd
from pprint import pprint
import requests
from bs4 import BeautifulSoup
import numpy as np

df = pd.read_csv('Data', encoding='1251')

pd.set_option('display.max_columns', None)
# print(df)

EMITENT_FULL_NAME = df['EMITENT_FULL_NAME']
DISCLOSURE_RF_INFO_PAGE = df['DISCLOSURE_RF_INFO_PAGE']
DISCLOSURE_RF_INFO_PAGE.fillna(0, inplace=True)

data = {'EMITENT_FULL_NAME': EMITENT_FULL_NAME, 'DISCLOSURE_RF_INFO_PAGE': DISCLOSURE_RF_INFO_PAGE}
inform_df = pd.DataFrame(data)
# print(inform_df)

inform_dict = inform_df.set_index('EMITENT_FULL_NAME').T.to_dict('list')
pprint(inform_dict)
# listik =[]
k = 0
for elem in inform_dict.keys():
    if inform_dict[elem][0] != 0 and "e-disclosure" not in inform_dict[elem][0]:
        k += 1
        print(inform_dict[elem][0])
        # if "https:" not in inform_dict[elem][0] and "http:" not in inform_dict[elem][0]:
        #     inform_dict[elem][0] = "https://" + inform_dict[elem][0]
        # url = inform_dict[elem][0]
        # response = requests.get(url)
        # soup = BeautifulSoup(response.text, 'lxml')
        # quotes = soup.find_all('span')
        # for elements in quotes:
        #     if "Отчетность" in elements:
        #         print(elements)
        #         listik.append(url)
        # print(len(listik))

print(k)
# print(listik)
