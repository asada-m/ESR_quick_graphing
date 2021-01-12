import os
import PySimpleGUI as sg
import ESR_graph_module as egm
from ESR_graph_layout import *

window = sg.Window('ESRスペクトルを50秒以内に作図するプログラム',LAYOUT,finalize=True)

graph_OK = False
save_OK = False
win2_active = False
filelist, file_use, file_use_list = [],[],[]
filelist_dat, file_use_dat, file_use_list_dat = [],[],[]
flist_DTADSC, flist_DAT = [],[]
resel = []
save_path = ''
isDTA=None

#Tab関係=====================================================
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
#データ選択===================================================
def add_files(isDTA):
    if isDTA == True:
        selected, list_A, list_B, allfiles = value['@liall'], file_use, file_use_list, flist_DTADSC
    else: selected, list_A, list_B, allfiles = value['@@liall'], file_use_dat, file_use_list_dat, flist_DAT
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
        if x in list_A:
            list_A.remove(x)
            for y in list_B:
                if y[0] == x:
                    y[-1] = ''
                    list_B.remove(y)
    return list_A,list_B

#順番入れ替え=================================================
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
#作図========================================================
def show_graph():
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
    return graph_OK

#色保存======================================================
def fixcolor(filelist):
    if len(filelist) <= MAX_DATALIST:
        y = len(filelist[0]) - 1 # datafileの最後がカラー情報
        usedcolorlist = [xfile[y] for xfile in filelist if xfile[y] in COLORFUL]
        availablecolor = [x for x in COLORFUL if x not in usedcolorlist]
        i = 0
        for x in range(len(filelist)):
            if filelist[x][y] == '':
                filelist[x][y] = availablecolor[i]
                i += 1
    return filelist

#データ保存==================================================
def save_a_data(mode):
    if mode == 'figure':
        global save_path
        ext = '.png'
        with open('tmp','rb') as f:
            savedata = f.read()
    else: return
    win2_active = True
    lyt = [[sg.Text('Folder',size=(7,1)),sg.InputText(save_path,k='@fol_save',size=(50,1),enable_events=True),sg.FolderBrowse(initial_folder=save_path)],
       [sg.Text('',size=(7,1)),sg.Listbox('',k='@savelist',size=(50,5),enable_events=True)],
       [sg.Text('Save as',size=(7,1)),sg.InputText('',k='@name',size=(50,1)),sg.Text(ext)],#sg.Combo([ext],size=(10,1),k='@ext',default_value=ext)],
       [sg.Button('save'), sg.Button('Exit')],]
    win2 = sg.Window('Save shown graph', lyt)
    while True:
        ev_save, val_save = win2.read()
        if ev_save in ('Exit', sg.WIN_CLOSED):
            win2.Close()
            win2_active = False
            break
        elif ev_save == '@fol_save':
            save_files = []
            try:
                files = [f for f in os.listdir(val_save['@fol_save']) if os.path.isfile(os.path.join(val_save['@fol_save'],f))]
                for xfile in files:
                    if xfile[-len(ext):] == ext: save_files.append(xfile)
            except: None
            win2['@savelist'].update(save_files)
        elif ev_save == '@savelist':
            win2['@name'].update(val_save['@savelist'][0][:-len(ext)])
        elif ev_save == 'save' and val_save['@name'] != '':
            sname = val_save['@name']+ ext
            if sname in save_files:
                sOK = sg.popup_ok_cancel(f'{sname}  exists. \n\nOverWrite ?')
                if sOK != 'OK': continue
            filename_s = val_save['@fol_save'] + '/' + val_save['@name'] + ext
            with open(filename_s,'wb') as fr:
                fr.write(savedata)
            save_path = val_save['@fol_save']
            sg.popup('Save complete')
            win2.Close()
            win2_active = False

#============================================================
while True:
    event,value = window.read()
#    Light = value['@light']
#    tab_update()
#    print(value['@light'])
    if event in (sg.WIN_CLOSED, 'Exit'): break
#フォルダ選択=================================================
    elif event == '@fol_read' and value['@fol_read']:
        flist_DTADSC = egm.folder_select(value['@fol_read'])
        filelist = []
        for x in flist_DTADSC:
            if egm.find_data(x,value) == True: filelist.append(x[0])
    elif event in ('@find_d','@find_a','@find_m'):
        filelist = []
        if event == '@find_d':
            file_use, file_use_list = [], []
            if value['@find_d'] == '2D':
                window['@liall'].update(select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)
            else: window['@liall'].update(select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED)
        for x in flist_DTADSC:
            if egm.find_data(x,value) == True: filelist.append(x[0])
    elif event == '@@fol_read' and value['@@fol_read']:
        flist_DAT = egm.folder_select_dat(value['@@fol_read'])
        filelist_dat = []
        for x in flist_DAT:
            if egm.find_data_dat(x,value) == True: filelist_dat.append(x[0])
    elif event == '@@find_free':
        filelist_dat = []
        for x in flist_DAT:
            if egm.find_data_dat(x,value) == True: filelist_dat.append(x[0])
#データ選択===================================================
    elif event == ' ↓ add ' and value['@liall'] != []:
        file_use,file_use_list = add_files(True)
    elif event == ' ↑ remove ' and value['@liuse'] != []:
        file_use,file_use_list = remove_files(True)
    elif event == '× Clear list':
        file_use, file_use_list = [], []
    elif event == '@@b_add' and value['@@liall'] != []:
        file_use_dat,file_use_list_dat = add_files(False)
    elif event == '@@b_remove' and value['@@liuse'] != []:
        file_use_dat,file_use_list_dat = remove_files(False)
    elif event == '@@b_clear':
        file_use_dat, file_use_list_dat = [], []
#順番入れ替え=================================================
    elif event == ' ↑ ' and value['@liuse'] != []:
        file_use, file_use_list, resel = order_up()
    elif event == ' ↓ ' and value['@liuse'] != []:
        file_use, file_use_list, resel = order_down()
    elif event == '@@b_up' and value['@@liuse'] != []:
        file_use_dat, file_use_list_dat, resel = order_up()
    elif event == '@@b_down' and value['@@liuse'] != []:
        file_use_dat, file_use_list_dat, resel = order_down()
#カラーの保存=================================================
    elif event == '@fixcol':
        for x in range(len(file_use_list)):
            file_use_list[x][6] = COLORFUL[x]
    elif event == '@fogcol':
        for xfile in file_use_list:
            xfile[6] = ''
    elif event == '@@fixcol':
        for x in range(len(file_use_list_dat)):
            file_use_list_dat[x][3] = COLORFUL[x]
    elif event == '@@fogcol':
        for xfile in file_use_list_dat:
            xfile[3] = ''
#図の作成=====================================================
    elif event == 'show':
        graph_OK = show_graph()
#図の保存=====================================================
    elif event == 'save figure' and graph_OK:
        save_a_data('figure')
#設定の保存==================================================
    elif event == 'save settings':
        save_ini(value)
        sg.popup('Save complete.','Settings are applied after restart application.')
    elif event == 'reset':
        window['@c_edit'].update(SETTING['DEFAULT']['Color'])
#オプションの読込と保存=======================================
    elif event == 'Load_options':
        update_options(window,value['@opt_load_name'])
    elif event == 'Save_options' and value['@opt_save_name'] != '':
        save_options(value['@opt_save_name'],value)
        window['@opt_load_name'].update(values=['DEFAULT']+FIGURE_OPTIONS.sections())
        window['@ini_figopt'].update(values=['DEFAULT']+FIGURE_OPTIONS.sections())
    elif event == 'Delete the option set':
        delete_option(value['@opt_load_name'])
        window['@opt_load_name'].update(values=['DEFAULT']+FIGURE_OPTIONS.sections())
        window['@ini_figopt'].update(values=['DEFAULT']+FIGURE_OPTIONS.sections())
        window['@opt_load_name'].update(value='')
####### 工事中 ##############################
    elif event == '@@mode' and value['@@mode'] in ('2D','1Dcomplex'):
        sg.popup('Sorry ! \n2D or 1Dcomplex graph is not available yet. ')
        window['@@mode'].update(value='1D')
    elif event == '@n_emx':
        window['@n_convtime'].update(value=False)
        window['@n_convtime'].update(disabled=True)
    elif event == '@n_other':
        window['@n_convtime'].update(disabled=False)
#リスト、図のアップデート====================================
    if event not in (' ↑ ',' ↓ ','@@b_up','@@b_down'): resel = []
    if event == '@mar_Xa':
        window['@mar'].update(value=value['@mar_Xa'])
        window['@@mar'].update(value=value['@mar_Xa'])
    elif event == '@mar':
        window['@mar_Xa'].update(value=value['@mar'])
        window['@@mar'].update(value=value['@mar'])
    elif event == '@@mar':
        window['@mar_Xa'].update(value=value['@@mar'])
        window['@mar'].update(value=value['@@mar'])
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

    if value['@light'] == False:
        graph_OK = show_graph()

#    print(isDTA)
window.close()

