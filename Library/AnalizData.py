import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import json
import zipfile
import tempfile
import pprint
import urllib.request
import time


keys = []
dir_list = []


def forming_dict():
    df = pd.read_csv(os.path.abspath('../Data/Data.csv'), encoding='1251')
    pd.set_option('display.max_columns', None)
    df = df[['EMITENT_FULL_NAME', 'DISCLOSURE_RF_INFO_PAGE']].drop_duplicates()
    # print(df)

    df['DISCLOSURE_RF_INFO_PAGE'].fillna(0, inplace=True)
    inform_dict = df.groupby(['EMITENT_FULL_NAME'])['DISCLOSURE_RF_INFO_PAGE'].apply(list).to_dict()
    url_dict = {}
    for elem in inform_dict.keys():
        if inform_dict[elem][0] != 0 and "www.e-disclosure.ru/" in inform_dict[elem][0] and \
                (inform_dict[elem][0] != 'https://www.e-disclosure.ru/' and inform_dict[elem][0] != 'www.e-disclosure.ru' and
                inform_dict[elem][0] != 'http://www.e-disclosure.ru/'):
            url_dict[elem] = inform_dict[elem][0]
    return url_dict

def saving(url):
    k = 0
    name = ''
    destination = ''
    for elem in url.keys():
        name = elem
        while ('"' in name):
            name = elem.replace('"', '')
        name = name.lstrip()
        name = name.rstrip()
        if os.path.exists(os.path.abspath('../Output') + '/' + name):
            print("in if")
            pass
        # print(os.path.exists(os.path.abspath('../Output') + '/'  + name))
        else:
            print('in else')
            os.mkdir(os.path.abspath('../Output') + '/' + name)
        print(f"name: {name}")
        print(os.path.abspath('../Output') + '/' + name)
        k = k + 1
        print('k = {}'.format(k))
        link = url[elem]
        response = requests.get(link)
        if "disclosure.skrin" in url[elem]:
            print(1)
            response.encoding = "windows 1251"
        soup = BeautifulSoup(response.text, 'lxml')
        print(0)
        if "disclosure.skrin" in url[elem]:
            # xpath = '//*[@id="td1"]'
            quotes = soup.findAll("a")
            for elements in quotes:
                string_united = ''
                string = str(elements)
                for i in string:
                    string_united = string_united + i
                if 'href="/disclosure_docs' in string_united:
                    start = string_united.find('/Год')
                    end = string_united.find('" target')
                    print(string_united[start:end])
                    start_url = string_united.find('="/')
                    destination = string_united[start+1:end]
                    url_to_download = 'https://disclosure.skrin.ru/' + string_united[start_url+3:end]
                    if " " in url_to_download:
                        url_to_download = url_to_download.replace(' ', '_')
                    print(url_to_download)
                    print(elem)
                    with open(os.path.abspath('../Output') + '/'  + name + '/' + destination, 'wb') as f:
                        destination = os.path.abspath('../Output') + '/'  + elem + '/' + destination
                        print('скачиваю')
                        ufr = requests.get(url_to_download)
                        print(f'urf: {ufr.content.decode("windows 1251")}')# делаем запрос
                        f.write(ufr.content)  # записываем содержимое в файл; как видите - content запроса
                    # wget.download(url, destination)
        if "e-disclosure" in url[elem]:
            print(2)
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
                    print(f'file: {fzip}')
                    while ('"' in elem):
                        elem = elem.replace('"', ' ')
                    fzip.extractall(os.path.abspath('../Output') + "/" + name)
                    file.close()
                    fzip.close()
                except zipfile.BadZipFile:
                    pass


def url_callback(urls):
    otch_dict = {}
    k = 0
    for elem in urls.keys():
        if ';' in urls[elem]:
            print('in ;')
            list_of_urls = urls[elem].split(';')
            for i in list_of_urls:
                if 'www.e-disclosure.ru/' in i:
                    print(f'i: {i}')
                    urls[elem] = i
        # time.sleep(0.2)
        k = k + 1
        print(f"elem: {urls[elem]}")
        print("k={}".format(k))
        if " " in urls[elem]:
            urls[elem] = urls[elem].replace(" ", '')
        if "https:" not in urls[elem] and "http:" not in urls[elem]:
            urls[elem] = "https://" + urls[elem]
            # print('2')
        url = urls[elem]
        print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('a')
        for elements in quotes:
            string_united = ''
            string = str(elements)
            for i in string:
                string_united = string_united + i
            if "Год" in string_united:
                first = string_united.find('"')
                second = string_united.find('">')
                first_amp = string_united.find('amp')
                second_amp = string_united.find(';type')
                string_united = string_united.replace(string_united[first_amp:second_amp+1], '')
                print("Добавил https://e-disclosure.ru/"+string_united[first+1:second-4])
                otch_dict[elem] = "https://e-disclosure.ru/"+string_united[first+1:second-4]

    return otch_dict


def search(urls):
    for elem in urls.keys():
        link = urls[elem]
        # print("Введите год, с которого начинается загрузка")
        # date_from = input()
        # print("Введите год, на котором закончится загрузка")
        # date_to = input()
        # print("Введите название компании, отчетность которой будет загружена")
        # company = input()
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('td')
        string_united = ''
        string = str(quotes)
        # print('5')
        for i in string:
            string_united = string_united + i
        # print(string_united)
        j = string_united.find('<td>20')
        print('j = {}'.format(j))
        pprint.pprint(string_united[j:len(string_united)])

def make_file(data):
    with open(os.path.abspath('../Data/List.json'), "w") as f:
        # for elem in urls_cleaned.keys():
        json.dump(data, f)


def read_file():
    with open(os.path.abspath('../Data/List.json'), "r") as f:
        list_info = json.load(f)
    return list_info


def make_dir_file():
    dir_list = os.listdir(os.path.abspath('../Output'))
    open(os.path.abspath('../Output/Folders.txt'), "w").close()
    with open(os.path.abspath('../Output/Folders.txt'), "w") as f:
        for elem in dir_list:
            if elem != 'Folders.txt':
                f.write(elem + '\n')


def download_listing():
    url = "https://www.moex.com/ru/listing/securities-list.aspx"
    link = ""

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.findAll("a")
    for elem in quotes:
        string_united = ''
        string = str(elem)
        for i in string:
            string_united = string_united + i
        if ">CSV (разделители - запятые)" in string_united:
            first = string_united.find('="') + 2
            last = string_united.find(">CSV (разделители - запятые)") - 1
            link = string_united[first:last]
            # link = link[1:len(link)-1]
            link = "https://www.moex.com/ru/listing/" + link
            print(link)

    destination = os.path.abspath('../Data/Data.csv')
    urllib.request.urlretrieve(link, destination)

