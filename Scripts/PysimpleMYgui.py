import PySimpleGUI as sg
import json
from .. import Library
# from ..AnalizData import url_callback, forming_dict, make_file
import os

url_dict = {}
path = os.getcwd()

if os.path.exists('C:\python\DataAnalizing\DataAnalizing\List.json'):
    with open('C:\python\DataAnalizing\DataAnalizing\List.json', "r") as f:
        companies_dict = json.load(f)

    companies_list = companies_dict.keys()

    print(companies_list)


    # col2 = sg.Column([[sg.Frame('Компании:', [[sg.Column([[sg.Listbox([str(i) for i in  companies_list],
    #                                                                   key='-ACCT-LIST-', size=(250, 437)), ]],
    #                                                      scrollable=True, size=(500, 600))]])]], pad=(0, 0))

    col2 = sg.Frame('Компании', [[sg.Listbox(companies_list, size=(150, 35), change_submits=True, key='-list-')]])
    button_download = sg.Button('Обновить данные')
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
        if event == 'Скачать данные':
            url_dict = forming_dict()
            url_callback(url_dict)
            make_file(url_dict)
else:
    text = sg.Text('Перед началом работы необходимо скачать данные. Для этого нажмите на кнопку.')
    button_download = [sg.Text(' ' * 45), sg.Button('Закачать данные')]                           
    layout = [[text], [button_download]]                                                          
    window = sg.Window('', layout)                                                                

    while True:                                                                                   
        event, values = window.read()                                                             
        if event == sg.WIN_CLOSED or event == 'Cancel':                                           
            break                                                                                 

    window.close()                                                                                
