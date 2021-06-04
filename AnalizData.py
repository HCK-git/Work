import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import json
import zipfile
import tempfile
import pprint

keys = []
df = pd.read_csv('Data', encoding='1251')
pd.set_option('display.max_columns', None)
df = df[['EMITENT_FULL_NAME', 'DISCLOSURE_RF_INFO_PAGE']].drop_duplicates()
# print(df)

df['DISCLOSURE_RF_INFO_PAGE'].fillna(0, inplace=True)
inform_dict = df.groupby(['EMITENT_FULL_NAME'])['DISCLOSURE_RF_INFO_PAGE'].apply(list).to_dict()
url_dict = {}
for elem in inform_dict.keys():
    if inform_dict[elem][0] != 0 and "e-disclosure" in inform_dict[elem][0]:
        url_dict[elem] = inform_dict[elem][0]


def saving(url):
    k = 0
    name = ''
    for elem in url.keys():
        name = elem
        while ('"' in name):
            print(elem)
            name = elem.replace('"', ' ')
        print(name)
        print("reporting/" + name)
        print(os.path.exists("reporting/" + name))
        if os.path.exists("reporting/" + name):
            print("in if")
            pass
        else:
            k = k + 1
            print('k = {}'.format(k))
            if "e-disclosure" in url[elem]:
                link = url[elem]
                response = requests.get(link)
                soup = BeautifulSoup(response.text, 'lxml')
                quotes = soup.findAll("a", {"class": "file-link"})
                # print(quotes)
                for elements in quotes:
                    string_united = ''
                    # print('4')
                    string = str(elements)
                    # print('5')
                    for i in string:
                        string_united = string_united + i
                    beg_url = string_united.find('href="http')+6
                    end_url = string_united.find('">')
                    response = requests.get(string_united[beg_url:end_url])
                    print(string_united[beg_url:end_url])
                    file = tempfile.TemporaryFile()
                    file.write(response.content)
                    try:
                        fzip = zipfile.ZipFile(file)
                        while ('"' in elem):
                            elem = elem.replace('"', ' ')
                            print(elem)
                        fzip.extractall("reporting/" + elem)
                        file.close()
                        fzip.close()
                    except zipfile.BadZipFile:
                        pass



def url_callback(urls):
    # pprint(inform_dict)
    otch_dict = {}
    k = 0
    for elem in urls.keys():

        k = k + 1
        print("k={}".format(k))
        # time.sleep(0.6)
        if " " in urls[elem]:
            urls[elem] = urls[elem].replace(" ", '')
        if "https:" not in urls[elem] and "http:" not in urls[elem]:
            urls[elem] = "https://" + urls[elem]
            # print('2')
        url = urls[elem]
        print("Рассматриваемый юрл {}".format(url))
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
                # print(string_united)
                first_amp = string_united.find('amp')
                second_amp = string_united.find(';type')
                string_united = string_united.replace(string_united[first_amp:second_amp+1], '')
                first = string_united.find('"')
                second = string_united.find('">')
                print("https://e-disclosure.ru/"+string_united[first+1:second])
                otch_dict[elem] = "https://e-disclosure.ru/"+string_united[first+1:second]
                # print('7')
    return otch_dict


def make_file(data):
    with open("List.json", "w") as f:
        # for elem in urls_cleaned.keys():
        json.dump(data, f)


def read_file():
    with open("List.json", "r") as f:
        list_info = json.load(f)
    return list_info


if os.path.exists("List.json"):
        urls_cleaned = read_file()
else:
    urls_cleaned = url_callback(url_dict)
    pprint.pprint(urls_cleaned)
    make_file(urls_cleaned)
saving(urls_cleaned)
