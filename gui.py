#-----------------------------#
# JackVesh IDE by iFanpS      #
# Still beta testing          #
#-----------------------------#

import PySimpleGUI as sg 
from tkinter import font as tkfont
from datetime import datetime
import sys

active = False

class RedirectObject:
    def __init__(jv, window):
        ''' Struct '''
        jv.window = window
        jv.saveout = sys.stdout
    
    def write(jvWrite, string):
        jvWrite.window['-BOX2-'].Widget.insert("end", string)
    
    def flush(flush):
        sys.stdout = flush.saveout 
        sys.stdout.flush()
    
save_setting = False

if save_setting == True:
    import shelve
    settings = shelve.open('config/jvide_settings')
else:
    settings = {} #Only save the change while the application is running
                  #When the application is not running it will reset to the default setting
                  
#-----------------------#
# Default setting       #
#-----------------------#
if len(settings.keys()) == 0:
    settings['theme'] = 'GrayGrayGray' # <- Default themes
    settings['themes'] = sg.list_of_look_and_feel_values()
    settings['font'] = ('Consolas', 11) # <- Default font
    settings['tabsize'] = 4 # <- Default indentation tabs
    settings['fname'] = None # <- if no file opened
    settings['value_box'] = ''
    settings['infos'] = 'Untitled'
    settings['version'] = '0.0.1'
    settings['out_box'] = ''
    settings['setting_out'] = ''
    
sg.change_look_and_feel(settings['theme']) # <- Default theme preview

strings = "Loaded settings:\n\t-> Themes: {}\n\t-> Font: {}\n\t-> Tabs: {}\n\t-> Version: {}"
settings.update(setting_out = strings.format(settings['theme'], settings['font'], settings['tabsize'], settings['version']))

def close_setting():
    settings.update(filename=None, body='', out='', infos='Untitled')
    if save_setting:
        settings.close() 
        
def window(settings):
    #-------------#
    # Main Window #
    #-------------#
    width = 80
    menu_layout = [
        ['File',['Open', 'Save', 'Close']],
        ['Edit',['Copy', 'Paste', 'Select all']],
        ['Format',['Tab','Auto formatting']],
        ['Setting',['Themes', sg.list_of_look_and_feel_values(), 'Font']]
    ]
    col1 = sg.Column([[sg.Multiline(default_text=settings['value_box'], font=settings['font'], key='-BOX-', size=(width,20))]])
    col2 = sg.Column([[sg.Multiline(default_text=settings['out_box'], font=settings['font'], key='-BOX2-', size=(width,8))]])
    
    window_layout = [
        [sg.Menu(menu_layout)],
        [sg.Text(settings['infos'], key='INFO_FILE', font=('Consolas', 11), size=(width,1))],
        [sg.Pane([col1, col2])]]
    
    window = sg.Window('JackVesh IDE', window_layout, resizable=True, margins=(0,0), return_keyboard_events=True)
    return window

#--------------------#
# Menu Structure     #
#--------------------#
def openfile(window):
    try:
        filename = sg.popup_get_file('File Name:', title='Open', no_window=True)
    except:
        return
    if filename not in (None,''):
        with open(filename,'r') as f:
            file_text = f.read()
        window['-BOX-'].update(value=file_text)
        window['INFO_FILE'].update(value='Loaded file: ' + filename.split('/')[-1])
        settings.update(filename=filename, body=file_text, infos=filename.split('/')[-1])
        
def savefile(window, values):
    filename = settings.get('fname')
    if filename not in (None,''):
        with open(filename,'w') as f:
            f.write(values['-BOX-'])
        window['INFO_FILE'](value=filename.split('/')[-1])
        settings.update(filename=filename, infos=filename.split('/')[-1])
    else:
        save_as(window, values)
        
def save_as(window, values):
    try: 
        filename = sg.popup_get_file('Save File', save_as=True, no_window=True)
    except:
        return
    if filename not in (None,''):
        with open(filename,'w') as f:
            f.write(values['-BOX-'])
        window['INFO_FILE'](value=filename.split('/')[-1])
        settings.update(filename=filename, infos=filename.split('/')[-1])
        
def copy(window, values):
    pass

#---------------------#
# Runner              #
#---------------------#

window = window(settings)
redir = RedirectObject(window)
sys.stdout = redir

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'Open':
        openfile(window)
    if event == 'Save':
        savefile(window, values)
