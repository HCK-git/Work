import urllib.request
import csv

destination = 'Data'
url = 'https://www.moex.com/ru/listing/securities-list-csv.aspx?type=1'
urllib.request.urlretrieve(url, destination)

with open("Data", encoding="windows-1251") as f:
    file_reader = csv.reader(f, delimiter=',')
    count = 0
    for row in file_reader:
        if count == 0:
            print("Файл имеет столбцы {}".format(", ".join(row)))
        else:
            print(row)
        count += 1
