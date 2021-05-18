import urllib.request
import csv

url = "https://www.moex.com/ru/listing/securities-list.aspx"

urllib.request.urlretrieve(url, 'pars.html')

with open('pars.html', 'r', encoding='utf-8') as f:
    html = f.read()
    first = html.find("Скачать данные в формате")
    last = html.find(">CSV (разделители - запятые)")
    link = html[first:last].split("<a href=")[1]
    link = link[1:len(link)-1]


link = "https://www.moex.com/ru/listing/" + link

destination = 'Data'
urllib.request.urlretrieve(link, destination)

with open("Data", encoding="windows-1251") as f:
    file_reader = csv.reader(f, delimiter=',')
    count = 0
    for row in file_reader:
        if count == 0:
            print("Файл имеет столбцы {}".format(", ".join(row)))
        else:
            print(row)
        count += 1