import PySimpleGUI as sg
import os
import sys
sys.path.append(os.path.abspath('../Library'))
import AnalizData
import pprint

url_dict = {}
path = os.getcwd()
selected_list = []
selected_dict = {}

if os.path.exists(os.path.abspath('../Data/List.json')):

    url_dict = AnalizData.read_file()

    companies_list = list(url_dict.keys())

    col2 = sg.Frame('Компании', [[sg.Listbox(values=companies_list, size=(150, 35), change_submits=True, key='companies', select_mode='multiple')]])
    button_download = sg.Button('Обновить данные')
    button_download_chosen = sg.Button('Скачать выбранное')
    buttons = sg.Column([[sg.Frame('Работа со всеми данными', [[sg.Button('Скачать все отчетности'), sg.Button('Обновить данные')]])],
                          [sg.Text(' '*10)],
                          [sg.Frame('Выборка данных', [[sg.Button('Скачать выбранное'), sg.Button('Сохранить выбор')]])]])
    # layout = [[col2, buttons]]
    sg.theme('DarkTeal10')
    layout = [[col2, buttons]]
    window = sg.Window('', layout)

    # Получение списка ключей, чтобы потом найти их значения и по ссылкам скачать файлы

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
        if event == 'Скачать все отчетности':
            AnalizData.saving(url_dict)
        if event == 'Сохранить выбор':
            for elem in values['companies']:
                selected_list.append(elem)
        if event == 'Скачать выбранное':
            pprint.pprint(f'selected_list: {selected_list}')
            for elem in selected_list:
                print(type(selected_list))
                print(type(elem))
                selected_dict[elem] = url_dict[elem]
            AnalizData.saving(selected_dict)


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