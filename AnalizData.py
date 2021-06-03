import pandas as pd
import requests
from bs4 import BeautifulSoup
import itertools
import multiprocessing
import os
import json
import zipfile
import tempfile


keys = []
df = pd.read_csv('Data', encoding='1251')
pd.set_option('display.max_columns', None)
df = df[['EMITENT_FULL_NAME', 'DISCLOSURE_RF_INFO_PAGE']].drop_duplicates()
# print(df)

df['DISCLOSURE_RF_INFO_PAGE'].fillna(0, inplace=True)
inform_dict = df.groupby(['EMITENT_FULL_NAME'])['DISCLOSURE_RF_INFO_PAGE'].apply(list).to_dict()
url_list = []
for elem in inform_dict.keys():
    if inform_dict[elem][0] != 0 and "e-disclosure" in inform_dict[elem][0]:
        url_list.append(inform_dict[elem])


def saving(url):
    for elem in url.keys():
        if "e-disclosure" in url[elem]:
            link = url[elem]
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'lxml')
            quotes = soup.findAll("a", {"class": "file-link"})
            print(quotes)
            for elements in quotes:
                string_united = ''
                # print('4')
                string = str(elements)
                # print('5')
                for i in string:
                    string_united = string_united + i
                beg_url = string_united.find('href="http')+6
                end_url = string_united.find('">')
                print(string_united[beg_url:end_url])
                response = requests.get(string_united[beg_url:end_url])
                file = tempfile.TemporaryFile()
                file.write(response.content)
                fzip = zipfile.ZipFile(file)
                fzip.extractall('Data/reporting/'+elem)
                file.close()
                fzip.close()


def url_callback(urls):
    # pprint(inform_dict)
    global keys
    otch_list = []
    k = 0
    for elem in urls:
        if " " in elem:
            elem = elem.replace(" ", '')
        if "https:" not in elem and "http:" not in elem:
            elem = "https://" + elem
            # print('2')
        url = elem
        print(url)
        response = requests.get(url)
        # print("2.1")
        # print('404')
        soup = BeautifulSoup(response.text, 'lxml')
        # print('505')
        quotes = soup.find_all('a')
        # print('3')
        for elements in quotes:
            string_united = ''
            # print('4')
            if "Годовая" in elements:
                string = str(elements)
                # print('5')
                for i in string:
                    string_united = string_united + i
                    # print('6')
                print(string_united)
                first_amp = string_united.find('amp')
                second_amp = string_united.find(';type')
                string_united = string_united.replace(string_united[first_amp:second_amp+1], '')
                first = string_united.find('"')
                second = string_united.find('">')
                print("https://e-disclosure.ru/"+string_united[first+1:second])
                otch_list.append("https://e-disclosure.ru/"+string_united[first+1:second])
                keys.append(elem)
                # print('7')
    return otch_list


def make_file(data):
    with open("List.json", "w") as f:
        # for elem in urls_cleaned.keys():
        json.dump(data, f)


def read_file():
    with open("List.json", "r") as f:
        list_info = json.load(f)
    return list_info


if __name__ == '__main__':
    companies_dict = {}
    if os.path.exists("List.json"):
        urls_cleaned = read_file()
    else:
        multiprocessing.freeze_support()
        mp = multiprocessing.Pool(processes=6)
        urls_with_reports = list(mp.imap_unordered(url_callback, url_list))
        # print('Length of value before: {}', format(len(urls_with_reports)))
        # urls_cleaned = list(itertools.chain(*urls_with_reports))
        print('Length of keys: {}', format(len(keys)))
        print('Length of value: {}', format(len(urls_with_reports)))
        for i in range(len(urls_with_reports)):
            companies_dict[keys[i]] = urls_with_reports[i]
        make_file(companies_dict)
    saving(companies_dict)
    # print(urls_cleaned)
