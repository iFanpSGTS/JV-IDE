#-----------------------------#
# JackVesh IDE by iFanpS      #
# Still beta testing          #
#-----------------------------#

import PySimpleGUI as sg 
from tkinter import font as tkfont
import clipboard as cb
import sys
from main import run_from_gui

active = False

class RedirectObject:
    def __init__(jv, window):
        ''' Struct '''
        jv.window = window
        jv.saveout = sys.stdout
    
    def write(jv, string):
        jv.window['-BOX2-'].Widget.insert("end", string)
    
    def flush(jv):
        sys.stdout = jv.saveout 
        sys.stdout.flush()
    
save_setting = False # <- Sometimes save is bug, idk why

if save_setting:
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
    settings['out_box'] = ''
    
sg.change_look_and_feel(settings['theme']) # <- Default theme preview

strings = "#-----------------------------------------#\nLoaded settings:\n\t-> Themes: {}\n\t-> Font: {}\n\t-> Tabs: {}\n\t-> File: {}\n#-----------------------------------------#\n"
settings.update(out_box = strings.format(settings['theme'], settings['font'], settings['tabsize'], settings['fname']))

def close_settings():
    settings.update(filename=None, value_box='', out_box='', infos='Untitled')
    if save_setting:
        settings.close()

def m_window(settings):
    #-------------#
    # Main Window #
    #-------------#
    width = 80
    menu_layout = [
        ['File',['Open', 'Save', 'Close file']],
        ['Edit',['Copy', 'Paste', 'Select all']],
        ['Format',['Tab','Auto formatting']],
        ['Run file',['RunFile']],
        ['Setting',['Themes', settings['themes'], 'Font']],
        ['About',['Help', 'About project']]
    ]
    
    col1 = sg.Column([[sg.Multiline(default_text=settings['value_box'], font=settings['font'], autoscroll=False, key='-BOX-', size=(width,20))]])
    col2 = sg.Column([[sg.Multiline(default_text=settings['out_box'], font=settings['font'], key='-BOX2-', autoscroll=True,size=(width,8))]])
    
    window_layout = [
        [sg.Menu(menu_layout)],
        [sg.Text(settings['infos'], key='INFO_FILE', font=('Consolas', 11), size=(width,1))],
        [sg.Pane([col1, col2])]]
    
    window = sg.Window('JackVesh IDE', window_layout, resizable=False, margins=(0,0), return_keyboard_events=True)
    return window

#--------------------#
# Menu Structure     #
#--------------------#
def openfile(window):
    try:
        filename = sg.popup_get_file('File Name:', title='Open', no_window=True, file_types=(("JackVesh", "*.jv"),))
    except:
        return
    if filename not in (None,''):
        with open(filename,'r') as f:
            file_text = f.read()
        window['-BOX-'].update(value=file_text)
        window['INFO_FILE'].update(value='Loaded file: ' + filename.split('/')[-1])
        settings.update(fname=filename, value_box=file_text, infos=filename.split('/')[-1])
        
def savefile(window, values):
    filename = settings.get('fname')
    if filename not in (None,''):
        with open(filename,'w') as f:
            f.write(values['-BOX-'])
        window['INFO_FILE'](value=filename.split('/')[-1])
        settings.update(fname=filename, infos=filename.split('/')[-1])
    else:
        save_as(window, values)
        
def save_as(window, values):
    try: 
        filename = sg.popup_get_file('Save File', save_as=True, no_window=True, default_extension='.jv', file_types=(("JackVesh", "*.jv"),))
    except:
        return
    if filename not in (None,''):
        with open(filename,'w') as f:
            f.write(values['-BOX-'])
        window['INFO_FILE'](value=filename.split('/')[-1])
        settings.update(fname=filename, infos=filename.split('/')[-1])

def closeFile(window):
    window['INFO_FILE'].update('Untitled')
    window['-BOX-'].update('')
 
def copy(values): # <- for now this function is used for the button.
                  # Basicly u just need to use CTRL+C, because now PySimpleGui already update the method!!
    copied_text = cb.copy(values['-BOX-'])
    return copied_text
    
def paste(window): # <- for now this function is used for the button.
                   # Basicly u just need to use CTRL+V, because now PySimpleGui already update the method!!
    try:
        clip = window.TKroot.clipboard_get()
    except:
        return
    else:
        window['-BOX-'].Widget.insert("insert", clip)
        
def select_all(window): # <- for now this function is used for the button.
                        # Basicly u just need to use CTRL+A, because now PySimpleGui already update the method!!
    window['-BOX-'].Widget.tag_add("sel","1.0","end")
    
def runJV(value, values):
    if values['fname'] == None:
        valueN = 'Untitled'
        run_from_gui(valueN, value['-BOX-'])
    else:
        valueN = values['fname'].split('/')[-1]
        run_from_gui(valueN, value['-BOX-'])

#---------------------#
# Settings Menu       #
#---------------------#
def changeTheme(window, event, values):
    settings.update(theme=event, value_box=values['-BOX-'], out_box=values['-BOX2-'])
    sg.change_look_and_feel(event)
    window.close()

def changeFont(window):
    font_name, font_size = settings.get('font')
    font_list = sorted([f for f in tkfont.families() if f[0]!='@'])
    if not font_name in font_list:
      font_name = font_list[0]
    font_sizes = [8,9,10,11,12,14]
    font_layout = [
        [sg.Combo(font_list, key='-FONT-', default_value=font_name), 
         sg.Combo(font_sizes, key='-SFONT-', default_value=font_size)],[sg.OK(), sg.Cancel()]]
    font_window = sg.Window('Font', font_layout, keep_on_top=True)
    font_event, font_values = font_window.read()
    if font_event not in (None,'Exit'):
        font_selection = (font_values['-FONT-'], font_values['-SFONT-'])
        if font_selection != settings['font']:
            settings.update(font=font_selection)
            window['-BOX-'].update(font=font_selection)
            window['-BOX2-'].update(font=font_selection)
            print(f"Font is changed from {(font_name, font_size)} to {font_selection}\n")
    font_window.close()
    
def changeTab(window):
    tab_layout = [[sg.Slider(range=(1,8), default_value=settings['tabsize'], orientation='horizontal', key='-SIZE-'), sg.OK(size=(5,2))]]
    tab_window = sg.Window('Tab Size', tab_layout, keep_on_top=True)
    tab_event, tab_values = tab_window.read()
    if tab_event not in (None, 'Exit'):
        old_tab_size = settings['tabsize']
        new_tab_size = int(tab_values['-SIZE-'])
        if new_tab_size != old_tab_size:
            settings.update(tabsize=new_tab_size)
            setTabs(window, new_tab_size)
            print(f"Tab size is changed from {old_tab_size} to {new_tab_size}\n")
    tab_window.close()
    
def setTabs(window, default_size=4):
    font = tkfont.Font(font=settings.get('font'))
    tab_width = font.measure(' '*default_size)
    window['-BOX-'].Widget.configure(tabs=(tab_width,)) 
    settings.update(tabsize=default_size)
    
def auto_formatting(): # Coming Soon
    pass

def helpS():
    help_text = """
This is GUI (Graphical User Interface) is used for editing JackVesh file & TXT file
This GUI helps you to run and edit JackVesh file, but for now you need to put this file in the same directory with JackVesh Intepreter
#------------------- How To Use ------------------#
 > Basicly this TextEditor is the same like every Simple TextEditor
 > You can see the Menu Bar (File, Edit, Format, Setting, About)
 > You can adjust the Tab by clicking on the Format Menu, and the Tab setting
 > You can change the Theme (broken) & the Font by clicking on the setting menu
 > Click about project if you want to know the UPDATE!!!
#------------------- How To Use ------------------#
"""
    sg.popup(help_text, title='Help',location=(0,0), keep_on_top=True)
    
def aboutProject():
    about = """
#--------------------------------------------------#  
I working on this project, (Q) Why? because GUI is easy way to understand
This project is currently beta, many thing i need to add on this GUI
If you want to Help me in this project you can make a PullRequest on my github repository
Discord: iFanpS
Github: iFanpSGTS
#--------------------------------------------------#    
"""
    sg.popup(about, title='Project', keep_on_top=True, location=(10,20))

# menu_layout = [
#         ['File',['Open', 'Save', 'Close file']],
#         ['Edit',['Copy', 'Paste', 'Select all']],
#         ['Format',['Tab','Auto formatting']],
#         ['Setting',['Themes', settings['themes'], 'Font']],
#         ['About',['Help', 'About project']]
#     ]


#---------------------#
# Runner              #
#---------------------#

window = m_window(settings)
redir = RedirectObject(window)
sys.stdout = redir

while True:
    event, values = window.read(timeout=1)
    if not active:
        active = True
        setTabs(window)
    
    if event in (None, 'Exit'):
        close_settings()
        break
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'Open':
        openfile(window)
    if event == 'Save':
        savefile(window, values)
    if event == ('Copy', 'c:67'):
        copy(values)
    if event == ('Paste', 'v:86'):
        paste(window)
    if event == ('Select all', 'a:65'):
        select_all(window)
    if event == 'Close file':
        closeFile(window)
    if event in settings['themes']:
        print(event)
        active == False
        changeTheme(window, event, values)
        sys.stdout = redir.saveout
        window = m_window(settings)
        redir = RedirectObject(window)
        sys.stdout = redir
    if event == 'Font':
        changeFont(window)
    if event == 'Tab':
        changeTab(window)
    if event == 'Help':
        helpS()
    if event == 'About project':
        aboutProject()
    if event == 'RunFile':
        runJV(values,settings)
        
