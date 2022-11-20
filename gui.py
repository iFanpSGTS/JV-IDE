import PySimpleGUI as sg
from pathlib import Path

sg.theme('GrayGrayGray')

menu_layout = [
    ['File',['Open', 'Save as', 'Close file']],
    ['Tools',['Calculator (Coming Soon)']],
    ['Run',['Run File']]
]

layout = [
    [sg.Menu(menu_layout)],
    [sg.Text('Untitled', key='-FNAME-')],
    [sg.Multiline(no_scrollbar=True, size=(100,35), key='-BOX-')]
]

window = sg.Window('JackVesh IDE', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    
    if event == 'Open':
        fpath = sg.popup_get_file('Open', no_window=True)
        if fpath:
            files = Path(fpath)
            window['-BOX-'].update(files.read_text())
            window['-FNAME-'].update(fpath.split('/')[-1])
            
    if event == 'Save as':
        fpath = sg.popup_get_file('Save as', no_window=True, save_as=True) + '.txt'
        files = Path(fpath)
        files.write_text(values['-BOX-'])
        window['-FNAME-'].update(fpath.split('/')[-1])
        
    if event == 'Close file':
        window['-BOX-'].update('')
        window['-FNAME-'].update('Untitled')