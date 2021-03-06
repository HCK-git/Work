import PySimpleGUI as sg
import os
import sys
sys.path.append(os.path.abspath('../Library'))
import DataAnalysis


url_dict = {}
url_dict_changed = {}
path = os.getcwd()
selected_list = []
selected_dict = {}

sg.theme('DarkBrown3')

if os.path.exists(os.path.abspath('../Data/List.json')):

    url_dict = DataAnalysis.read_file()

    companies_list = list(url_dict.keys())

    col2 = sg.Frame('Компании', [[sg.Listbox(values=companies_list, size=(150, 35), change_submits=True,
                                             key='companies', select_mode='multiple')]])
    buttons = sg.Column([[sg.Frame('Работа со всеми данными',
                         [[sg.Button('Скачать все отчетности'), sg.Button('Обновить список компаний')]])],
                         [sg.Text(' '*10)], [sg.Frame('Выборка данных', [[sg.Button('Сохранить выбор'),
                                                                         sg.Button('Скачать выбранное')]])]])
    layout = [[col2, buttons]]
    window = sg.Window('', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Обновить список компаний':
            DataAnalysis.download_listing()
            DataAnalysis.forming_dict()
            url_dict = DataAnalysis.forming_dict()
            url_dict_changed = DataAnalysis.site_parsing(url_dict)
            DataAnalysis.make_file(url_dict_changed)
        if event == 'Скачать все отчетности':
            DataAnalysis.saving(url_dict)
            DataAnalysis.make_dir_file()
        if event == 'Сохранить выбор':
            selected_list = []
            for elem in values['companies']:
                selected_list.append(elem)
        if event == 'Скачать выбранное':
            selected_dict = {}
            for elem in selected_list:
                selected_dict[elem] = url_dict[elem]
            DataAnalysis.saving(selected_dict)
            DataAnalysis.make_dir_file()

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
            DataAnalysis.download_listing()
            DataAnalysis.forming_dict()
            url_dict = DataAnalysis.forming_dict()
            url_dict_changed = DataAnalysis.site_parsing(url_dict)
            DataAnalysis.make_file(url_dict_changed)

    window.close()
