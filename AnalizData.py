import pandas as pd
from pprint import pprint
import requests
from bs4 import BeautifulSoup
import numpy as np
import itertools
import multiprocessing



df = pd.read_csv('Data', encoding='1251')
pd.set_option('display.max_columns', None)
df = df[['EMITENT_FULL_NAME','DISCLOSURE_RF_INFO_PAGE']].drop_duplicates()
# print(df)

df['DISCLOSURE_RF_INFO_PAGE'].fillna(0, inplace=True)
inform_dict = df.groupby(['EMITENT_FULL_NAME'])['DISCLOSURE_RF_INFO_PAGE'].apply(list).to_dict()
url_list = []
for elem in inform_dict.keys():
    if inform_dict[elem][0] != 0 and "e-disclosure" in inform_dict[elem][0]:
        url_list.append(inform_dict[elem])
# pprint(url_list)




def url_callback(urls):

    # pprint(inform_dict)
    listik = []
    k = 0
    for elem in urls:
        # k += 1
        # print(inform_dict[elem][0])
        if "https:" not in elem and "http:" not in elem:
            elem = "https://" + elem
        url = elem
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('a')
        for elements in quotes:
            string_united = ''
            if "Годовая" in elements:
                string = str(elements)
                for i in string:
                    string_united = string_united + i
                first_amp = string_united.find('amp')
                second_amp = string_united.find(';type')
                string_united = string_united.replace(string_united[first_amp:second_amp+1], '')
                first = string_united.find('"')
                second = string_united.find('">')
                listik.append(string_united)
    return listik


if __name__ == '__main__':
    multiprocessing.freeze_support()
    mp = multiprocessing.Pool(processes=16)
    urls_with_reports = mp.imap_unordered(url_callback, url_list)
    urls_cleaned = set( itertools.chain(*urls_with_reports))
    print(urls_cleaned)


