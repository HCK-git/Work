import PySimpleGUI as sg
import json

with open('C:\python\DataAnalizing\DataAnalizing\List.json', "r") as f:
    companies_dict = json.load(f)

companies_list = companies_dict.keys()

print(companies_list)


# col2 = sg.Column([[sg.Frame('Компании:', [[sg.Column([[sg.Listbox([str(i) for i in  companies_list],
#                                                                   key='-ACCT-LIST-', size=(250, 437)), ]],
#                                                      scrollable=True, size=(500, 600))]])]], pad=(0, 0))

col2 = sg.Frame('Компании', [[sg.Listbox(companies_list, size=(150, 35), change_submits=True, key='-list-')]])
button_download = sg.Button('Скачать данные')
button_download_chosen = sg.Button('Скачать выбранное')
buttons = sg.Column([[sg.Button('Скачать данные')],
                      [sg.Button('Скачать выбранное')]])
layout = [[col2, buttons]]

window = sg.Window('Trying to show list', layout)

while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED:
        break