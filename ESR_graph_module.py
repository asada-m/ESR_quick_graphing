import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker, cm
from ESR_graph_layout import COLORFUL

#COLOR_COLORFUL = ['black','red','blue','limegreen','darkorange','magenta','deepskyblue','green','gray','blueviolet']

#DSCデータ読み込み============================================
def __read_DSC_file(DSC_filename_fullpath):
    param = {}
    is_state = 64 # all:64 Mani:32 Pulse:16 2D:8 END:4 Time:2 fs:1 
    with open(DSC_filename_fullpath) as f:
        allLines = f.read().splitlines()
    for x in range(len(allLines)):
        line = allLines[x]
        if line == '' : continue
        if line[-1]=='\\' and x < len(allLines): #\で終わるとき行を結合する
            allLines[x+1] = line[0:-1]+allLines[x+1]
            allLines[x]=''
            continue
#                line.replace(line[-1],'')
        if len(line)>1: line[-2:].replace('\\n','\n')#改行を改行に変換
        Key = line.split(None,1)[0]
        if len(line.split(None,1)) == 1: Value = ''
        if len(line.split(None,1)) > 1: Value = line.split(None,1)[1]#最初の区切り１つで分割
        if Key == '': continue
        if Key[0].isalpha() == 0:
            if Key == '#MHL':
                is_state += 32
                break
            continue
        Value = Value.strip()#両端のwhitespaceを削除
        Value = Value.strip("'")#両端の''を削除
        param[Key]=Value
    if ('XNAM' in param and param['XNAM'] == 'Field') or ('YNAM' in param and param['YNAM'] == 'Field'): is_state += 1
    if ('XNAM' in param and param['XNAM'] == 'Time') or ('YNAM' in param and param['YNAM'] == 'Time') or ('XUNI' in param and param['XUNI'] == 'ns'): is_state += 2
    if 'XNAM' in param and param['XNAM'] == 'RF': is_state += 4
    if ('XPTS' in param and float(param['XPTS']) > 1) and ('YPTS' in param and float(param['YPTS']) > 1): is_state += 8
    if 'EXPT' in param and param['EXPT'] == 'PLS': is_state += 16
    return param, is_state
# param:  dictionary{'Key':'Value'} Value=''のこともある
# err_text: 'error message'
#=============================================================
#フォルダ選択=================================================
def folder_select(folder_path):
    try: files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path,f))]
    except: return []
    filelist_DTA, filelist_DSC, flist_DTADSC = [],[],[]
    for x in files:
        if len(x) < 4: continue
        if x[-4:]=='.DTA' or x[-4:]=='.dta':
            filelist_DTA.append(x)
        elif x[-4:]=='.DSC' or x[-4:]=='.dsc':
            filelist_DSC.append(x)
    for x in filelist_DTA:
        for y in filelist_DSC:
            if x[:-4] == y[:-4]:
                para, is_state = __read_DSC_file(folder_path+'/'+y)
                flist_DTADSC.append([x[:-4], x, y, para, folder_path, is_state, ''])
    return flist_DTADSC
# folder_path:  full path
# flist_DTADSC: ['filename_base', 'filename_DTA', 'filename_DSC', param{dictionary}, folder_path, type, color]

def folder_select_dat(folder_path):
    try: files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path,f))]
    except: return '', []
    filelist_dat = []
    for x in files:
        if len(x) < 4: continue
        if x[-4:]=='.DAT' or x[-4:]=='.dat':
            filelist_dat.append([x[:-4], x, folder_path, ''])
    return filelist_dat
# flist_dat: ['filename_base', 'filename_dat', folder_path, color]
#=============================================================
#検索=========================================================
def find_data(xfile, value):
# all:64 Mani:32 Pulse:16 2D:8 END:4 Time:2 fs:1 
    sel_mode_dim, sel_mode_axis, sel_mode_mani = value['@find_d'],value['@find_a'],value['@find_m']
    if   sel_mode_dim == '1D' and xfile[5] & 8: return False
    elif sel_mode_dim == '2D' and not xfile[5] & 8: return False
    if   sel_mode_mani == 'Raw data' and xfile[5] & 32: return False
    elif sel_mode_mani == 'Manipulated' and not xfile[5] & 32: return False
    elif sel_mode_mani == 'CW' and xfile[5] & 16: return False
    elif sel_mode_mani == 'Pulse' and not xfile[5] & 16: return False
    elif sel_mode_mani not in ('all','Raw data','Manipulated','CW','Pulse'):
        sel_keyword = sel_mode_mani.split(' ')
        for x in sel_keyword:
            if x not in xfile[0]: return False
    sel_m = {'all':64,'Fieldsweep':1,'Timescan':2,'ENDOR':4,'2D':8,'Pulse':16,'Manipulated':32}
    if sel_mode_axis in sel_m.keys() and not xfile[5] & sel_m[sel_mode_axis]: return False
    return True
def find_data_dat(xfile,value):
    sel_keyword = value['@@find_free'].split(' ')
    for x in sel_keyword:
        if x not in xfile[0]: return False
    return True
#=============================================================
#DTAデータ読み込み for graphs====================================
def load_BES3T(file_info):
# folder_path: 'C:/user/.../...'
# file_info: ['file_base', 'file_base.DTA', 'file_base.DSC', param{dictionary}]
    folder_path = file_info[4]
    fn_DTA = folder_path +'\\'+ file_info[1]
    param = file_info[3]
    abs_y, err_text, is_err = [], '', False
    if 'IKKF' in param and param['IKKF'] != '':
        parts_par = param['IKKF'].split(',')
        nDataValue = len(parts_par)
        isComp = [0]*nDataValue
        for i in range(nDataValue):
            if   parts_par[i] == 'CPLX': isComp[i] = 1
            elif parts_par[i] == 'REAL': isComp[i] = 0
            else:
                err_text += 'Error: '+file_info[2]+' Unknown IKKF data\n'
                is_err=True
    else: # assume real
        err_txt += 'Warning: '+file_info[2]+' No IKKF: assuming REAL\n'
        isComp = [0]
        nDataValue = 1

    if 'XPTS' in param: nx = int(param['XPTS'])
    else: err_text += file_info[2]+' XPTS not found'
    if 'YPTS' in param: ny = int(param['YPTS'])
    else: ny = 1
    if 'ZPTS' in param: nz = int(param['ZPTS'])
    else: nz = 1
    Dimensions = (nx,ny,nz)

    if 'BSEQ' in param:
        if   param['BSEQ'] == 'BIG': BytO = '>' #'ieee-be'
        elif param['BSEQ'] == 'LIT': BytO = '<' #'ieee-le'
        else:
            err_text += 'Error: '+file_info[2]+' Unknown BSEQ type\n'
            is_err=True
    else: BytO = '>' # assume BIG

    if 'IRFMT' in param:
        parts_par = param['IRFMT'].split(',')
        if len(parts_par) != nDataValue:
            err_text += 'Error: '+file_info[2]+' Inconsistent IKKF and IRFMT\n'
            is_err=True
        for i in range(nDataValue):
            if   parts_par[i].upper() == 'C': NumberFormat = 'b' #'int8'signed 1byte int
            elif parts_par[i].upper() == 'S': NumberFormat = 'h' #'int16'signed 2byte int
            elif parts_par[i].upper() == 'I': NumberFormat = 'l' #'int32'signed 4byte int
            elif parts_par[i].upper() == 'F' and isComp[i] == 0: NumberFormat = 'f' #'float32'float 4byte
            elif parts_par[i].upper() == 'F' and isComp[i] == 1: NumberFormat = 'c8' #'complex64'two-float32 complex
            elif parts_par[i].upper() == 'D' and isComp[i] == 0: NumberFormat = 'd' #'float64'float 8byte
            elif parts_par[i].upper() == 'D' and isComp[i] == 1: NumberFormat = 'c16' #'complex128'two-float64 complex(python default)
            elif parts_par[i].upper() in ['A', 'O', 'N']:
                err_text += 'Error: '+file_info[2]+' Not BES3T data\n'
                is_err=True
            else:
                err_text += 'Error: '+file_info[2]+' Unknown IRFMT type\n'
                is_err=True
    else:
        err_text += 'Error: '+file_info[2]+' IRFMT not found\n'
        is_err=True
    if 'IIFMT' in param:
        if param['IIFMT'].upper() != param['IRFMT'].upper():
            err_text += 'Error: '+file_info[2]+' IRFMT and IIFMT must be identical\n'
            is_err=True

    AxisNames = ('X','Y','Z')
    minimum, Width = [0]*3, [0]*3
    abscissa = [0]*3
    for i in range(3):
        if Dimensions[i]<=1: continue
        AxisType = param[AxisNames[i]+'TYP']
        if AxisType == 'IGD':
            compFN = folder_path +'/'+ file_info[0] +'.'+ AxisNames[i] + 'GF'
            DataFormat = param[AxisNames[i]+'FMT']
            if   DataFormat.upper() == 'D': sourceFormat = 'd' #'float64'
            elif DataFormat.upper() == 'F': sourceFormat = 'f' #'float32'
            elif DataFormat.upper() == 'I': sourceFormat = 'l' #'int32'
            elif DataFormat.upper() == 'S': sourceFormat = 'h' #'int16'
            else:
                err_text += 'Error: '+file_info[2]+' Unknown XYZ Data format\n'
                is_err=True
            if os.path.isfile(compFN):
                with open(compFN, 'rb') as fg:
                    abscissa[i] = np.fromfile(fg, BytO + sourceFormat)
            else: AxisType = 'IDX' # if fg cannot open: assume Axistype=IDX
        if AxisType == 'IDX':
            minimum[i] = float(param[AxisNames[i]+'MIN'])
            Width[i] = float(param[AxisNames[i]+'WID'])
            if Width[i] == 0:
                err_text += 'Warning: '+file_info[2]+' Zero Width\n'# warning
                minimum[i] = 1
                Width[i] = Dimensions[i]-1
            abscissa[i] = minimum[i] + np.linspace(0,Width[i],Dimensions[i])
        elif AxisType == 'NTUP':
            err_text += 'Error: '+file_info[2]+' cannot read NTUP axis\n'
            is_err=True
        GN = AxisNames[i]+'NAM'

    Data_matrix_R, Data_matrix_I = [],[]
    with open(fn_DTA, 'rb') as fg:
        Data_matrix = np.fromfile(fg, BytO + NumberFormat)
    # 1D
    if   Dimensions[2] ==1 and Dimensions[1] ==1:
        abs_x = abscissa[0]
        if isComp[0] == 0:
            Data_matrix_R = np.vstack([abs_x,Data_matrix]).T
        elif isComp[0] == 1:
            Data_matrix_R = np.vstack([abs_x,Data_matrix.real,Data_matrix.imag]).T
    # 2D
    elif Dimensions[2] ==1 and Dimensions[1] >1:
        Data_matrix = Data_matrix.reshape(Dimensions[1],Dimensions[0])
        kado = np.array([0])
        abs_x = abscissa[0]
        abs_y = abscissa[1]
        Data_matrix_R = np.vstack([abs_x,Data_matrix.real])
        Data_matrix_R = Data_matrix_R.T
        if isComp[0] == 1:
            Data_matrix_I = np.vstack([abs_x,Data_matrix.imag])
            Data_matrix_I = Data_matrix_I.T

    else: # Dimensions[2] >1:# 3D data
        err_text += 'Error: '+file_info[0]+' 3D data cannot convert\n'
        is_err=True
    return Dimensions, abs_x, abs_y, Data_matrix, err_text, is_err

#    if mode == 'plot':
#        if data_y==[]: data_y = abscissa[1]
#        return Dimensions, abs_x, abs_y, Data_matrix, err_text, is_err, xg, yg
#        if Dimensions[2] ==1 and Dimensions[1] >1:
#            return Dimensions, abs_x, abs_y, Data_matrix, err_text, is_err, xg, yg
#        else:
#            return Dimensions, abs_x, data_y, Data_matrix, err_text, is_err, xg, yg
#    else:
#        return Data_matrix_R, Data_matrix_I, data_y, text_head, err_text, is_err
# Data_matrix = array[1D or 2D, real or complex]
#=============================================================
#datデータ読み込み for graphs====================================
def load_dat(file_info):
    fullname = file_info[2] + '\\' + file_info[1]
    try:
        with open(fullname, 'r') as f:
            allLines = f.read().splitlines()
    except:
        return None, None, f'{file_info[1]} cannot be read.\n'
    abs_x, data_r = [],[]
    for i in range(len(allLines)):
        if ',' in allLines[0]:
            d = allLines[i].split(',')
        else:
            d = allLines[i].split()
        if len(d) == 0: return None
        elif len(d) == 1:
            abs_x.append(i)
            data_r.append(float(d[0]))
        else:
            abs_x.append(float(d[0]))
            data_r.append(float(d[1]))
    return np.array(abs_x), np.array(data_r), None
# ひとまず1D dataのみ
#=============================================================
#=============================================================
#リストのx軸が同じかチェック==================================
def check_axis(flist):
    if   len(flist) == 0: return False
    elif len(flist) == 1: return True
    elif len(flist) > 1:
        if 'XUNI' in flist[0][3]: ch_x = flist[0][3]['XUNI']
        for x in flist:
            if 'XUNI' in x[3] and x[3]['XUNI'] != ch_x: return False
        return True
#valueからオプション設定=======================================
def v_to_opt(value,file,isDTA):
    opt = {}
    y = 6 if isDTA == True else 3
    a = '' if isDTA == True else '@'
    if value['@c_black'] == True:
        opt['c'] = ['black','black','black','black','black','black','black','black','black','black']
    else:
        opt['c'] = []
        if file[0][y] != '':
            for x in range(len(file)):
                if file[x][y] != '': opt['c'].append(file[x][y])
                else:opt['c'].append(COLORFUL[x])
        else: opt['c'] = COLORFUL
    if value['@size_tate'] == True:
        opt['size'], opt['dpi'] = (5.0,7.0), 100.0
    elif value['@size_yoko'] == True:
        opt['size'], opt['dpi'] = (7.0,5.0), 100.0
    elif value['@size_manual'] == True:
        try: opt['size'] = (float(value['@size_MX']),float(value['@size_MY']))
        except: opt['size'] = (7.0,5.0)
        try: opt['dpi'] = float(value['size_dpi'])
        except: opt['dpi'] = 100.0
    else: opt['size'], opt['dpi'] = (7.0,5.0), 100.0
    opt['grid'] = True if value['@grid'] == True else False
    opt['t'] = True if value['@tight'] == True else False
    opt['mar_xr'] = value['@mar_XR']/100
    opt['mar_xl'] = value['@mar_XL']/100
    opt['mar_y'] = value['@mar_Ya']/100
    opt['y'] = False if value[a+'@noysc'] == True else True
    opt['stack'] = value[a+'@stk']/100
    opt['margin'] = value[a+'@mar']/100
    if 'Bottom' in value[a+'@cpos']: opt['posV'] = ['top',-1]
    else: opt['posV'] = ['bottom',1]
    if 'Right' in value[a+'@cpos']: opt['posH'] = ['right',-1,0.98,-1]
    else: opt['posH'] = ['left',1,0.02,0]
    if value[a+'@ctype'] == 'Spectrum': opt['ctyp'] = 'spectrum'
    else: opt['ctyp'] = 'list'
    if   value[a+'@csize'] == 'large': opt['csize'] = [18.0,0.015,0.08]
    elif value[a+'@csize'] == 'medium': opt['csize'] = [14.0,0.015,0.06]
    else: opt['csize'] = [10.0,0.015,0.04]
    
    if isDTA == True:
        if   value['@normal'] == True:
            opt['n'] = 'Normal'
            opt['nn'] = 32
            if value['@n_power'] == True: opt['nn'] += 1
            if value['@n_gain'] == True: opt['nn'] += 2
            if value['@n_convtime'] == True: opt['nn'] += 4
            if value['@n_scans'] == True: opt['nn'] += 8
        elif value['@same'] == True: opt['n'] = 'Ignore'
        else: opt['n'] = 'None'
        if   value['@capt'] == 'File name': opt['capt'] = 'file'
        elif value['@capt'] == 'Data name': opt['capt'] = 'TITL'
        elif value['@capt'] == 'Microwave Frequency': opt['capt'] = 'MWFQ'
        elif value['@capt'] == 'Microwave Power': opt['capt'] = 'Power'
        elif value['@capt'] == '(Manual)':
            opt['capt'] = 'My'
            opt['capt_my'] = value['@capt_my']
        else: opt['capt'] = 'None'
        if 'IRNAM' in file[0][3]:
            opt['ylabel'] = f"{file[0][3]['IRNAM']}"
        else: opt['ylabel'] = ''
        if 'XNAM' in file[0][3] and 'XUNI' in file[0][3]:
            opt['xlabel'] = f"{file[0][3]['XNAM']} ({file[0][3]['XUNI']})"
        else: opt['xlabel'] = ''
    else:# dat
        if value['@@same'] == True: opt['n'] = 'Ignore'
        else: opt['n'] = 'None'
        opt['xlabel'] = value['@@xnam'] if value['@@xnam'] != 'None' else ''
        opt['ylabel'] = value['@@ynam'] if value['@@ynam'] != 'None' else ''
        if   value['@@capt'] == 'File name': opt['capt'] = 'file'
        elif value['@@capt'] == '(Manual)':
            opt['capt'] = 'My'
            opt['capt_my'] = value['@@capt_my']
        else: opt['capt'] = 'None'
    
#    if value['@g_cal'] == True:##############
#        opt['gfactor'] = 2 if value['@g_adjustg'] == True else 1
#    else: opt['gfactor'] = 0
    return opt

def make_captions(opt,file):
    capt = []
    if opt['capt'] == 'file':
        for x in file: capt.append(x[0])
    elif opt['capt'] == 'None':
        for x in file: capt.append('')
    elif opt['capt'] == 'MWFQ':
        for x in file:
            if opt['capt'] in x[3]:
                mw = float(x[3][opt['capt']])/ 1e9# add
                capt.append(f"{mw:.3f} GHz")
            else: capt.append('')
    elif opt['capt'] == 'My':
        capt = opt['capt_my'].split(';')
        if len(capt)<len(file):
            for i in range(len(file)-len(capt)):
                capt.append('')
    else:
        for x in file:
            if opt['capt'] in x[3]: capt.append(x[3][opt['capt']])
            else: capt.append('')
    return capt
#データの規格化===============================================
def Normalize(dataR,param,opt,isDTA=True):
    if isDTA and opt['n'] == 'Normal': #easyspin先輩がやってるの真似する
        if opt['nn'] & 8 and 'AVGS' in param: N = float(param['AVGS'])
        else: N = 1
        if opt['nn'] & 4 and 'SPTP' in param: CT = float(param['SPTP'])*1000
        else: CT = 1
        if opt['nn'] & 2 and 'RCAG' in param: G = 10**float(param['RCAG'])/20
        else: G = 1
        if opt['nn'] & 1 and 'MWPW' in param: P = float(param['MWPW'])*1000
        else: P = 1
        dataR = dataR / N / G / CT / (P*P)
    elif isDTA and opt['n'] == 'Ignore': #最大最小値を1,-1または1,0に設定
        if 'EXPT' in param and param['EXPT'] == 'CW':
            if 'XNAM' in param and param['XNAM'] == 'Field':
                ysize, base = 2, -1
            else: ysize, base = 1, 0
        else: ysize, base = 1, 0
        ymax,ymin = np.amax(dataR), np.amin(dataR)
        dataR = (dataR - ymin) / (ymax - ymin) *ysize +base
    elif isDTA == False and opt['n'] == 'Ignore': #最大最小値を1,-1に設定
        ymax,ymin = np.amax(dataR), np.amin(dataR)
        dataR = (dataR - ymin) / (ymax - ymin) *2 -1
    else: None
    return dataR
#補正したデータリスト作成=====================================
def make_data_list(filelist,opt,isDTA=True):
    err = ''
    datalist, Datax,Datay, sa = [],[],[],[]
    for xfile in filelist:
        if isDTA == True:
            _, abs_x, _, Data_matrix, err_text, is_err = load_BES3T(xfile)
#        Dim, abs_x, abs_y, Data_matrix, err_text, is_err = load_BES3T(xfile)
            if is_err == True: err += err_text
            tmp_y = Normalize(Data_matrix.real, xfile[3],opt,True)
        else:
            abs_x, Data_matrix, err_text = load_dat(xfile)
            if err_text: return None,err_text
            if Data_matrix != []:
                tmp_y = Normalize(Data_matrix,None,opt,False)
            else: tmp_y = 0
        Datay.append(tmp_y)
        Datax.append(abs_x)
        sa.append(np.amax(tmp_y) - np.amin(tmp_y))
    maxheight = max(sa)* opt['stack']
    for c in range(len(filelist)):
        Datay[c] = Datay[c] - maxheight * c
        datalist.append([Datax[c], Datay[c]])
    # datalist[index] = [x[i], data_r[i]]
    return datalist, err

def get_xpos(xl,xwid,opt,DL):
    tx = xl[0]+xwid*opt['posH'][2]
    if opt['posH'][0] == 'left':
        if DL[0][0] > tx: xpos = DL[0][0]
        else: xpos = tx
    elif opt['posH'][0] == 'right':
        if DL[0][-1] < tx: xpos = DL[0][-1]
        else: xpos = tx
    return xpos

def get_ypos(DLc,opt,tlength,ywid,xpos,xl):
    shifty = opt['posV'][1]*ywid*0.02
    is_b = True if opt['posV'][0]=='bottom' else False
    is_t = True if opt['posV'][0]=='top' else False
    newDL = []
    if opt['posH'][0]=='right':
        xmin, xmax = xpos-tlength, xl[1]
    else:
        xmin, xmax = xl[0], xpos+tlength
    for w in range(len(DLc[0])):
        if xmin <= DLc[0][w] <= xmax:
             newDL.append(DLc[1][w])
    ypos = newDL[opt['posH'][1]]
    for y in newDL:
        if is_b and y > ypos: ypos = y
        if is_t and y < ypos: ypos = y
    return ypos + shifty

# 複数グラフの表示============================================
# 1D data のみ可能
def graph_1D(file,value,isDTA):
    if isDTA == True: 
        if check_axis(file)==False: return 'All data must have the same X-axis. '
    elif isDTA == None: return 'Data type (DTA or dat) unknown'
    opt = v_to_opt(value,file,isDTA)
    try:
        DL,err = make_data_list(file,opt,isDTA)
        if err: return err
    except: return 'Data file cannot be read.'
    capt = make_captions(opt,file)
    fig, ax = plt.subplots(figsize=opt['size'],dpi=opt['dpi'])
    ax.set_xmargin(opt['margin'])
    ax.set_ymargin(opt['mar_y'])
    ax.tick_params(labelsize=opt['csize'][0])
    plt.xlabel('',fontsize=opt['csize'][0])
    plt.ylabel('',fontsize=opt['csize'][0])
    if opt['grid']==True: ax.grid()
    if opt['y']==False: 
        ax.tick_params(labelleft=False)
        ax.tick_params(labelright=False)
        ax.set_yticks([])
    if opt['t']==True: fig.tight_layout()
    ax.set(ylabel=opt['ylabel'])
    ax.set(xlabel=opt['xlabel'])
    cnt = len(file)
    for c in range(cnt):
        ax.plot(DL[c][0], DL[c][1], color=opt['c'][c])
    xl, yl = ax.get_xlim(), ax.get_ylim()
    xl_l = xl[0]+(xl[1]-xl[0])*opt['mar_xl']
    xl_r = xl[1]-(xl[1]-xl[0])*opt['mar_xr']
    ax.set_xlim(xl_l,xl_r)
    xl, yl = ax.get_xlim(), ax.get_ylim()
    xwid, ywid= xl[1]-xl[0], yl[1]-yl[0]
    for c in range(cnt):
        if opt['ctyp'] == 'spectrum':
            xpos = get_xpos(xl,xwid,opt,DL[c])
            if opt['size']==(5,7): tlength = xwid*opt['csize'][1]*len(capt[c])
            else: tlength = xwid*opt['csize'][1]*len(capt[c])
            ypos = get_ypos(DL[c],opt,tlength,ywid,xpos,xl)
        else: # listのとき
            xpos = xl[0]+xwid*opt['posH'][2]
            if opt['posV'][0] == 'bottom':#upper
                ypos = yl[1]-opt['csize'][2]*ywid*(c+1)-ywid*0.03
            else:#down
                ypos = yl[0]+opt['csize'][2]*ywid*(cnt-c)+ywid*0.03
        ax.text(xpos, ypos,capt[c], ha=opt['posH'][0],va=opt['posV'][0],color=opt['c'][c],fontsize=opt['csize'][0])
    if opt['size']==(5,7):
        ax.xaxis.set_major_locator(ticker.MaxNLocator(6,steps=[1,2,2.5,5,10]))
    if opt['n'] == 'Normal': plt.title('** Normalized by parameters **',y=1)# ↑にシフトするときはy=1.08
    elif opt['n'] == 'Ignore': plt.title('** Normalized by max/min intensity **',y=1)
#    if opt['gfactor'] > 0:##################
#        axg = ax.twiny()
#        axg.set_xlabel('g-factor',fontsize=opt['csize'][0])
#        axg.tick_params(labelsize=opt['csize'][0])
#        mw = float(file[0][3]['MWFQ'])/1e9*714.418
#        gl_min, gl_max = mw/xl[0], mw/xl[1]
#        axg.set_xlim([gl_min,gl_max])
    plt.savefig('tmp',format='png')
    plt.close()
    return None
#=============================================================
# 2D dataの表示 (1 file only)#####################################
def graph_2D(file,value,isDTA):
    file = file[0]
    fig, ax = plt.subplots(figsize=opt['size'])
    ax.set_xmargin(opt['margin'])
    plt.xlabel('',fontsize=opt['csize'][0])
    plt.ylabel('',fontsize=opt['csize'][0])
    if opt['g']==True: ax.grid()
    if opt['y']==False: 
        ax.tick_params(labelleft=False)
        ax.tick_params(labelright=False)
        ax.set_yticks([])
    if opt['t']==True: fig.tight_layout()
    if 'IRNAM' in file[3]:
        ax.set(ylabel=f"{file[3]['IRNAM']}")
    if 'XNAM' in file[3] and 'XUNI' in file[3]:
        ax.set(xlabel=f"{file[3]['XNAM']} ({file[3]['XUNI']})")
    return None
#=============================================================
#=============================================================
