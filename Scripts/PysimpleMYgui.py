import PySimpleGUI as sg
import json
# import os
# from ..Library import AnalizData
import os
import sys
sys.path.append(os.path.abspath('../Library'))
import AnalizData


import pprint
url_dict = {}
path = os.getcwd()


if os.path.exists(os.path.abspath('../Data/List.json')):
    # with open(os.path.abspath('../Data/List.json'), "r") as f:
    #     companies_dict = json.load(f)
    url_dict = AnalizData.read_file()

    companies_list = url_dict.keys()

    # print(companies_list)


    # col2 = sg.Column([[sg.Frame('Компании:', [[sg.Column([[sg.Listbox([str(i) for i in  companies_list],
    #                                                                   key='-ACCT-LIST-', size=(250, 437)), ]],
    #                                                      scrollable=True, size=(500, 600))]])]], pad=(0, 0))

    col2 = sg.Frame('Компании', [[sg.Listbox(companies_list, size=(150, 35), change_submits=True, key='-list-', select_mode='multiple')]])
    button_download = sg.Button('Обновить данные')
    button_download_chosen = sg.Button('Скачать выбранное')
    buttons = sg.Column([[sg.Button('Скачать отчетности')],
                          [sg.Button('Обновить данные')],
                          [sg.Button('Скачать выбранное')]])
    # layout = [[col2, buttons]]
    layout = [[col2, buttons]]
    window = sg.Window('', layout)

    # Получение списка ключей, чтобы потом найти их значения и по ссылкам скачать файлы
    selected_list = window.read()

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break
        if event == 'Обновить данные':
            AnalizData.forming_dict()
            url_dict = AnalizData.forming_dict()
            AnalizData.url_callback(url_dict)
            AnalizData.make_file(url_dict)
        if event == 'Скачать отчетности':
            AnalizData.saving(url_dict)
        if event == 'Скачать выбранное':
            # Попытка вывести элементы листа
            for elem in selected_list:
                pprint.pprint(elem)


else:
    text = sg.Text('Перед началом работы необходимо скачать данные. Для этого нажмите на кнопку.')
    button_download = [sg.Text(' ' * 45), sg.Button('Скачать данные')]
    layout = [[text], [button_download]]
    window = sg.Window('', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        if event == 'Скачать данные':
            AnalizData.forming_dict()
            url_dict = AnalizData.forming_dict()
            AnalizData.url_callback(url_dict)
            AnalizData.make_file(url_dict)

    window.close()