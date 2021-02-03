"""
ESR quick graphing ver 1.06 (2021/02/03)
Main loop and functions related to GUI window
"""
import os
import webbrowser
import PySimpleGUI as sg
import ESR_graph_module as egm
from ESR_graph_layout import *

window = sg.Window(APP_TITLE,LAYOUT,finalize=True)
window['@link'].set_cursor(cursor='hand2') # mouse-over events
window['@link2'].set_cursor(cursor='hand2')

graph_OK = False
file = ''
win2_active, win3_active, win4_active = False, False, False
filelist, file_use, file_use_list = [],[],[]
filelist_dat, file_use_dat, file_use_list_dat = [],[],[]
flist_DTADSC, flist_DAT = [],[]
resel = []
save_path = ''
isDTA=None
state_all, state_staged = 0,0

# Tab  =====================================================
def tab_update():
    if file_use == []:
        window['TAB_dat'].update(disabled=False)
    if file_use_dat == []:
        window['TAB_dta'].update(disabled=False)
    if file_use == [] and file_use_dat == []:
        isDTA = None
    if file_use != []:
        window['TAB_dat'].update(disabled=True)
        isDTA = True
    if file_use_dat != []:
        window['TAB_dta'].update(disabled=True)
        isDTA = False
    return isDTA
# options ============================================
def update_enable_options():
    global state_staged
    state_staged = 0
    if file_use_list != []:
        for xfile in file_use_list:
            for y in (1,2,4,8,16,32,64):
                if xfile[5] & y and not state_staged & y: state_staged += y
    if state_staged & 1:
        window['@g_adjust'].update(disabled=False)
    else:
        window['@g_adjust'].update(disabled=True)
    if state_staged & 8:
        for x in ('@same','@normal','@no','@fixcol','@fogcol','@noysc','@capt','@csize','@capt_my','@ctype','@cpos','@stk'):
            window[x].update(disabled=True)
#        window['@2D_text'].update(visible=True)
#        window['@2D_slice'].update(visible=True)
    else:
        for x in ('@same','@normal','@no','@fixcol','@fogcol','@noysc','@capt','@csize','@capt_my','@ctype','@cpos','@stk'):
            window[x].update(disabled=False)
#        window['@2D_text'].update(visible=False)
#        window['@2D_slice'].update(visible=False)
    if state_staged & 64:
        window['@imag'].update(disabled=False)
    else:
        window['@imag'].update(disabled=True, value=False)
        value['@imag'] = False

def update_margin(xpar, ypar, separate):
    window['@mar_XL'].update(value=xpar)
    window['@mar_XR'].update(value=xpar)
#    window['@mar_Ya'].update(value=ypar)
    window['@mar_YL'].update(value=ypar)
    window['@mar_YH'].update(value=ypar)
    window['@stk'].update(value=separate)
#    value['@mar_XL'],value['@mar_XR'],value['@mar_Ya'],value['@stk'] = xpar,xpar,ypar,separate
    value['@mar_XL'],value['@mar_XR'],value['@mar_YL'],value['@mar_YH'],value['@stk'] = xpar,xpar,ypar,ypar,separate

# select data ===================================================
def add_files(selected, isDTA):
    if isDTA == True:
        list_A, list_B, allfiles = file_use, file_use_list, flist_DTADSC
    else: list_A, list_B, allfiles = file_use_dat, file_use_list_dat, flist_DAT
    for x in selected:
        if x not in list_A:
            list_A.append(x)
            for y in allfiles:
                if y[0] == x: list_B.append(y)
    return list_A,list_B

def remove_files(isDTA):
    if isDTA == True:
        selected, list_A, list_B = value['@liuse'], file_use, file_use_list
    else: selected, list_A, list_B = value['@@liuse'], file_use_dat, file_use_list_dat
    for x in selected:
        for a , b in zip(list_A, list_B):
            if x == a:
                list_A.remove(a)
                b[-1] = ''
                list_B.remove(b)
    return list_A,list_B


# change order of data list========================================
def order_up():
    if isDTA == True:
        selected, list_A, list_B = value['@liuse'], file_use, file_use_list
    else: selected, list_A, list_B = value['@@liuse'], file_use_dat, file_use_list_dat
    if selected[0] != list_A[0]:
        for x in selected:
            for i in range(len(list_A)):
                if i == 0: continue
                if list_A[i] == x:
                    list_A[i-1], list_A[i] = list_A[i], list_A[i-1]
                    list_B[i-1], list_B[i] = list_B[i], list_B[i-1]
        resel = selected
    else: resel = []
    return list_A,list_B,resel

def order_down():
    if isDTA == True:
        selected, list_A, list_B = value['@liuse'], file_use, file_use_list
    else: selected, list_A, list_B = value['@@liuse'], file_use_dat, file_use_list_dat
    if selected[-1] != list_A[-1]:
        for x in reversed(selected):
            for i in reversed(range(len(list_A))):
                if i == len(list_A)-1: continue
                if list_A[i] == x:
                    list_A[i+1], list_A[i] = list_A[i], list_A[i+1]
                    list_B[i+1], list_B[i] = list_B[i], list_B[i+1]
        resel = selected
    else: resel = []
    return list_A,list_B,resel
# graphing ========================================================
def show_graph():
    global graph_OK
    if isDTA == True:
        file_g = file_use_list
        check_dim = value['@find_d']
    elif isDTA == False:
        file_g = file_use_list_dat
        check_dim = value['@@mode']
    else: file_g = []
    if file_g == []:
        graph_OK = False
    elif len(file_g) > MAX_DATALIST:
        sg.popup('Error:  Too many data files')
        graph_OK = False
    else:
        if   check_dim == '1D': err = egm.graph_1D(file_g,value,isDTA)
        elif check_dim == '2D': err = egm.graph_2D(file_g,value,isDTA)
        if err:
            sg.popup('error',err)
            graph_OK = False
        else: graph_OK = True
    if graph_OK:
        window['@imgraph'].update(filename='tmp')
    else: 
        window['@imgraph'].update(data=nograph)

# fix color order ================================================
def fixcolor(filelist):
    usedcolorlist = [xfile[-1] for xfile in filelist if xfile[-1] in COLORFUL]
    availablecolor = [x for x in COLORFUL if x not in usedcolorlist]
    i = 0
    for xfile in filelist:
        if xfile[-1] == '':
            try:
                xfile[-1] = availablecolor[i]
                i += 1
            except:
                xfile[-1] = 'black'
    return filelist

# save graph file ==================================================
def read_filelist(pathname,extension):# search png in folder
    listup_files = []
    try:
        files = [f for f in os.listdir(pathname) if os.path.isfile(os.path.join(pathname,f))]
        for xfile in files:
            if xfile[-len(extension):] == extension: listup_files.append(xfile)
    except: pass
    return listup_files

def save_a_data():
    global save_path
    ext = '.png'
    with open('tmp','rb') as f:
        savedata = f.read()
    win2_active = True
    save_files = read_filelist(save_path,ext)
    lyt = [[sg.Text('Folder',size=(7,1)),sg.InputText(save_path,k='@fol_save',size=(40,1),enable_events=True),sg.FolderBrowse(initial_folder=save_path)],
       [sg.Text('',size=(7,1)),sg.Listbox(save_files,k='@savelist',size=(40,5),enable_events=True)],
       [sg.Text('Save as',size=(7,1)),sg.InputText('',k='@name',size=(40,1)),sg.Text(ext)],#sg.Combo([ext],size=(10,1),k='@ext',default_value=ext)],
       [sg.Button('save'), sg.Button('Exit')],]
#       [sg.Button('save'), sg.Button('output python commands',k='@b_matpl',button_color=white_bcolor), sg.Button('Exit')],]
    win2 = sg.Window('Save shown graph', lyt)
    while True:
        ev_save, val_save = win2.read()
        if ev_save in ('Exit', sg.WIN_CLOSED):
            win2.Close()
            win2_active = False
            break
        elif ev_save == '@fol_save' and val_save['@fol_save'] != '':
            save_files = read_filelist(val_save['@fol_save'],ext)
            win2['@savelist'].update(save_files)
        elif ev_save == '@savelist' and val_save['@savelist'] != []:
            win2['@name'].update(val_save['@savelist'][0][:-len(ext)])
        elif ev_save == 'save' and val_save['@fol_save'] != '' and val_save['@name'] != '':
            sname = val_save['@name']+ ext
            if sname in save_files:
                sOK = sg.popup_ok_cancel(f'" {sname} " exists. \n\nOverWrite ?')
                if sOK != 'OK': continue
            filename_s = val_save['@fol_save'] + '/' + val_save['@name'] + ext
            try:
                with open(filename_s,'wb') as fr:
                    fr.write(savedata)
            except: sg.popup('error: folder cannot be open')
            save_path = val_save['@fol_save']
            sg.popup('Save complete')
            win2.Close()
            win2_active = False
            break

def save_options(value):
    win3_active = True
    lyt = [[sg.Text('Save Current Figure Options as:')],
    [sg.InputText('',k='@opt_save_name',size=(24,1))],
    [sg.Button('OK'),sg.Button('Cancel')],]
    win3 = sg.Window('Save figure option',lyt)
    while True:
        ev_fopt,val_fopt = win3.read()
        if ev_fopt in ('Cancel',sg.WIN_CLOSED):
            break
        elif ev_fopt == 'OK' and val_fopt['@opt_save_name'] != '':
            if save_options_pop(val_fopt['@opt_save_name'],value) == True:
                break
    win3.Close()
    win3_active = False

def show_parameter(files):
    win4_active = True
    lists = []
    para = ('TITL','DATE','TIME','FrequencyMon','Power','PowerAtten','Gain','ModAmp','ConvTime','TimeConst','SweepTime','QValue','NbScansDone')
    name = ('File name','Data name','Date','Time','MWfrequency','MWPower','MWAtten','Gain','ModAmp','ConvTime','TimeConst','SweepTime','Q-value','Scans')
    lists = [[xfile[0]] + [xfile[3][param] if param in xfile[3] else '-' for param in para] for xfile in files]
    lyt = [[sg.Table(lists,headings=name,vertical_scroll_only=False)],
    [sg.Button('OK')],]
    win4 = sg.Window('Parameters',lyt)
    while True:
        ev, val = win4.read()
        if ev in ('OK',sg.WIN_CLOSED):
            break
    win4.Close()
    win4_active = False

# main loop =================================================
while True:
    event,value = window.read()
#    print(event)
    if event in (sg.WIN_CLOSED, 'Exit'): break
# select folder =================================================
    elif event == '@fol_browse':
        file = sg.PopupGetFile('Browse',
            file_types=(('BES3T parameter files','*.DSC'),('BES3T data files','*.DTA'),('All','*.*')),
            no_window=True,initial_folder=ini_fo)
        if file == '': continue
        ini_fo = None
        folder = os.path.dirname(file)
        value['@fol_read'] = folder
        window['@fol_read'].update(value=folder)
        # read files
        flist_DTADSC = egm.folder_select(value['@fol_read'])
        filelist = []
        if flist_DTADSC and not flist_DTADSC[0]: continue
        for x in flist_DTADSC:
            if egm.find_data(x,value) == True: filelist.append(x[0])
        # add selected file
        if egm.DTADSC_exists(folder,file) == True:
            file_base = os.path.basename(file)[:-4]
            file_use,file_use_list = add_files([file_base],True)
            update_enable_options()
            if state_staged & 8: update_margin(0,0,0)
    elif event == '@fol_read' and value['@fol_read']:
        flist_DTADSC = egm.folder_select(value['@fol_read'])
        filelist = []
        if flist_DTADSC and not flist_DTADSC[0]: continue
        for x in flist_DTADSC:
            if egm.find_data(x,value) == True: filelist.append(x[0])
    elif event in ('@find_d','@find_a','@find_m'):
        if flist_DTADSC and not flist_DTADSC[0]: continue
        filelist = []
        if event == '@find_d':
            file_use, file_use_list = [], []
            if value['@find_d'] == '2D':
                window['@liall'].update(select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)
                MAX_DATALIST = 1
            else:
                window['@liall'].update(select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED)
                MAX_DATALIST = 20 #temp
        for x in flist_DTADSC:
            if egm.find_data(x,value) == True: filelist.append(x[0])
    elif event == '@@fol_browse':
        file = sg.PopupGetFile('Browse',
            file_types=(('Data files','*.dat'),('All','*.*')),
            no_window=True,initial_folder=ini_fo)
        if file == '': continue
        ini_fo = None
        folder = os.path.dirname(file)
        value['@@fol_read'] = folder
        window['@@fol_read'].update(value=folder)
        # read files
        flist_DAT = egm.folder_select_dat(value['@@fol_read'])
        filelist_dat = []
        if flist_DAT and not flist_DAT[0]: continue
        for x in flist_DAT:
            if egm.find_data_dat(x,value) == True: filelist_dat.append(x[0])
        # add selected file
        if os.path.splitext(file)[1] in ('.DAT','.dat'):
            file = os.path.basename(file)[:-4]
            file_use_dat,file_use_list_dat = add_files([file],False)
    elif event == '@@fol_read' and value['@@fol_read']:
        flist_DAT = egm.folder_select_dat(value['@@fol_read'])
        filelist_dat = []
        if flist_DAT and not flist_DAT[0]: continue
        for x in flist_DAT:
            if egm.find_data_dat(x,value) == True: filelist_dat.append(x[0])
#        window['@@fol_browse'].InitialFolder = None
    elif event == '@@find_free':
        if flist_DAT and not flist_DAT[0]: continue
        filelist_dat = []
        for x in flist_DAT:
            if egm.find_data_dat(x,value) == True: filelist_dat.append(x[0])
# select data ===================================================
    elif event in (' ↓ add ', '@liall') and value['@liall'] != []:
        file_use,file_use_list = add_files(value['@liall'],True)
        update_enable_options()
        if state_staged & 8: update_margin(0,0,0)
    elif event in (' ↑ remove ', '@liuse') and value['@liuse'] != []:
        file_use,file_use_list = remove_files(True)
        update_enable_options()
    elif event == '× Clear list':
        file_use, file_use_list = [], []
        update_enable_options()
    elif event in ('@@b_add', '@@liall') and value['@@liall'] != []:
        file_use_dat,file_use_list_dat = add_files(value['@@liall'],False)
    elif event in ('@@b_remove', '@@liuse') and value['@@liuse'] != []:
        file_use_dat,file_use_list_dat = remove_files(False)
    elif event == '@@b_clear':
        file_use_dat, file_use_list_dat = [], []
# change order =================================================
    elif event == ' ↑ ' and value['@liuse'] != []:
        file_use, file_use_list, resel = order_up()
    elif event == ' ↓ ' and value['@liuse'] != []:
        file_use, file_use_list, resel = order_down()
    elif event == '@@b_up' and value['@@liuse'] != []:
        file_use_dat, file_use_list_dat, resel = order_up()
    elif event == '@@b_down' and value['@@liuse'] != []:
        file_use_dat, file_use_list_dat, resel = order_down()
# color order =================================================
    elif event == '@fixcol':
        for i, xfile in enumerate(file_use_list):
            if i < len(COLORFUL):
                xfile[6] = COLORFUL[i]
            else:
                xfile[6] = 'black'
    elif event == '@fogcol':
        for xfile in file_use_list:
            xfile[6] = ''
    elif event == '@@fixcol':
        for i, xfile in enumerate(file_use_list_dat):
            if i < len(COLORFUL):
                xfile[3] = COLORFUL[i]
            else:
                xfile[3] = 'black'
    elif event == '@@fogcol':
        for xfile in file_use_list_dat:
            xfile[3] = ''
# make and save graph ==========================================
    elif event == 'refresh':
        show_graph()
    elif event == 'save figure' and graph_OK:
        save_a_data()
# save settings ==================================================
    elif event == 'save settings':
        if not value['@s_filerow'].isdecimal():
            value['@s_filerow'] = file_row
        if not value['@s_datarow'].isdecimal():
            value['@s_datarow'] = data_row
        if int(value['@s_filerow']) < 2: value['@s_filerow'] = 2
        if int(value['@s_datarow']) < 2: value['@s_datarow'] = 2
        window['@s_datarow'].update(value=value['@s_datarow'])
        window['@s_filerow'].update(value=value['@s_filerow'])
        save_ini(value)
        sg.popup('Save complete.','Settings are applied after restart application.')
    elif event == '@b_col_reset':
        window['@c_edit'].update(SETTING['DEFAULT']['Color'])
# load/save figure options======================================
    elif event == '@b_load_options' and value['@opt_load_name'] != '':
        if update_options(window,value) == False:
            window['@opt_load_name'].update(value='')
    elif event == '@b_save_options':
        save_options(value)
        window['@opt_load_name'].update(values=['DEFAULT']+FIGURE_OPTIONS.sections())
        window['@ini_figopt'].update(values=['DEFAULT']+FIGURE_OPTIONS.sections())
    elif event == '@delete_option_set' and value['@opt_load_name'] != '':
        delete_option(value['@opt_load_name'])
        window['@opt_load_name'].update(values=['DEFAULT']+FIGURE_OPTIONS.sections())
        window['@ini_figopt'].update(values=['DEFAULT']+FIGURE_OPTIONS.sections())
        window['@opt_load_name'].update(value='')
# slider ===================================================
    elif event == '@b_mar_reset':
        update_margin(0,0,0) if state_staged & 8 else update_margin(5,5,0)
# DSC parameter list ===========================================
    elif event == 'parameter' and file_use_list != []:
        show_parameter(file_use_list)
# open links in browser ========================================
    elif event == '@link':
        webbrowser.open('https://matplotlib.org/3.3.3/gallery/color/named_colors.html')
    elif event == '@link2':
        webbrowser.open('https://github.com/asada-m/ESR_quick_graphing')
####### under construction ##############################
    elif event == '@@mode' and value['@@mode'] != '1D':
        sg.popup('Sorry ! \n2D mode is not available yet. ')
        window['@@mode'].update(value='1D')
#    elif event == '@n_emx':
#        window['@n_convtime'].update(value=False)
#        window['@n_convtime'].update(disabled=True)
#    elif event == '@n_other':
#        window['@n_convtime'].update(disabled=False)
#    elif event == '@b_matpl':
#        sg.popup_scrolled()
# update list and figure ====================================
    if event not in (' ↑ ',' ↓ ','@@b_up','@@b_down'): resel = []
    window['@liall'].update(filelist)
    window['@liuse'].update(file_use)
    window['@@liall'].update(filelist_dat)
    window['@@liuse'].update(file_use_dat)
    isDTA = tab_update()
    if isDTA == True:
        window['@liuse'].SetValue(resel)
    elif isDTA == False:
        window['@@liuse'].SetValue(resel)
    if value['@fixcol'] and file_use_list != []:
        file_use_list = fixcolor(file_use_list)
    elif value['@@fixcol'] and file_use_list_dat != []:
        file_use_list_dat = fixcolor(file_use_list_dat)
    if len(file_use) >= MAX_DATALIST:
          window[' ↓ add '].update(disabled=True)
    else: window[' ↓ add '].update(disabled=False)
    if len(file_use_dat) >= MAX_DATALIST:
          window['@@b_add'].update(disabled=True)
    else: window['@@b_add'].update(disabled=False)

    if value['@light'] == False and event not in ('refresh','save figure','@link','@link2','parameter'):
        show_graph()

window.close()

