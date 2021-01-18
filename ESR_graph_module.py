"""
ESR quick graphing ver 1.03 (2021/01/18)
functions for loading data and graphing
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker, cm
from ESR_graph_layout import COLORFUL

# load DSC data ============================================
def __read_DSC_file(DSC_filename_fullpath):
    param = {}
    is_state = 256 # all:256 Complex:64 Mani:32 Pulse:16 2D:8 END:4 Time:2 fs:1 
    with open(DSC_filename_fullpath) as f:
        allLines = f.read().splitlines()
    for x in range((DSClength := len(allLines))):
        line = allLines[x]
        if line == '' : continue
        if line[-1]=='\\' and x < DSClength:
            allLines[x+1] = line[0:-1]+allLines[x+1]
            allLines[x]=''
            continue
#                line.replace(line[-1],'')
        if len(line)>1: line[-2:].replace('\\n','\n')
        Key = (linesplit := line.split(None,1))[0]
        splitsize = len(linesplit)
        if splitsize == 1: Value = ''
        if splitsize > 1:  Value = linesplit[1]
        if Key == '': continue
        if Key[0].isalpha() == 0:
            if Key == '#MHL':
                is_state += 32
                break
            continue
        Value = Value.strip()
        Value = Value.strip("'")
        param[Key]=Value
    for x in ('XNAM','XUNI','IRNAM','IRUNI'):
        if x not in param: param[x] = ''
    if param['XNAM'] == 'Field' or ('YNAM' in param and param['YNAM'] == 'Field'): is_state += 1
    if param['XNAM'] == 'Time' or ('YNAM' in param and param['YNAM'] == 'Time') or param['XUNI'] == 'ns': is_state += 2
    if 'XNAM' in param and param['XNAM'] == 'RF': is_state += 4
    if ('XPTS' in param and float(param['XPTS']) > 1) and ('YPTS' in param and float(param['YPTS']) > 1): is_state += 8
    if 'EXPT' in param and param['EXPT'] == 'PLS': is_state += 16
    if 'IKKF' in param and param['IKKF'] == 'CPLX': is_state += 64
    return param, is_state
# param:  dictionary{'Key':'Value'}
# err_text: 'error message'
#=============================================================
# select folder ==============================================
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
# search =========================================================
def find_data(xfile, value):
# all:256 Complex:64 Mani:32 Pulse:16 2D:8 END:4 Time:2 fs:1 
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
    sel_m = {'all':256,'Fieldsweep':1,'Timescan':2,'ENDOR':4,'2D':8,'Pulse':16,'Manipulated':32}
    if sel_mode_axis in sel_m.keys() and not xfile[5] & sel_m[sel_mode_axis]: return False
    return True

def find_data_dat(xfile,value):
    sel_keyword = value['@@find_free'].split(' ')
    for x in sel_keyword:
        if x not in xfile[0]: return False
    return True
#=============================================================
# load DTA for graphs====================================
def load_BES3T(file_info,opt):
# file_info: ['file_base', 'file_base.DTA', 'file_base.DSC', param{dictionary}, 'C:/user/...','datatype']
    folder_path = file_info[4]
    fn_DTA = folder_path +'/'+ file_info[1]
    param = file_info[3]
    abs_x, abs_y, err_text, is_err = [], [], '', False
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
    abscissa, abs_g = [0]*3,[[],[],[]]
    xg, yg =False,False
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
        if opt['gfactor']==True and GN in param and param[GN]=='Field':
            try:
                for j in range(len(abscissa[i])):
                    jiba = abscissa[i][j] + opt['g_mod']
                    abscissa[i][j] = jiba # save MODIFIED field 
                    abs_g[i].append(float(param['MWFQ']) / jiba * 714.418 /1e+9)
                if i==0: xg=True
                elif i==1: yg=True
            except: err_text += 'Warning: '+file_info[0]+' Cannot make g-factor axis\n'

    with open(fn_DTA, 'rb') as fg:
        Data_matrix = np.fromfile(fg, BytO + NumberFormat)
    # 1D
    if   Dimensions[2] ==1 and Dimensions[1] ==1:
        if xg == True:
            abs_x = abs_g[0]
        else:
            abs_x = abscissa[0]
    # 2D
    elif Dimensions[2] ==1 and Dimensions[1] >1:
        Data_matrix = Data_matrix.reshape(Dimensions[1],Dimensions[0])
        Data_matrix = Data_matrix.real
#        if xg == True:
#            abs_x = abs_g[0]
#        else: abs_x = abscissa[0]
#        if yg == True:
#            abs_y = abs_g[0]
#        else: abs_y = abscissa[1]
        abs_x, abs_y = abscissa[0], abscissa[1]
    else: # Dimensions[2] >1:# 3D data
        err_text += 'Error: '+file_info[0]+' 3D data cannot convert\n'
        is_err=True
    return abs_x, abs_y, Data_matrix, err_text, is_err
# Data_matrix = array[1D or 2D, real or complex]
#=============================================================
# load dat data for graph ====================================
def load_dat(file_info):
    fullname = file_info[2] + '/' + file_info[1]
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
        len_d = len(d)
        if len_d == 0: return None
        elif len_d == 1:
            abs_x.append(i)
            data_r.append(float(d[0]))
        else:
            abs_x.append(float(d[0]))
#            for j in range(1,1+min([len(d),opt['column']])):
            data_r.append(float(d[1]))##########
    return np.array(abs_x), np.array(data_r), None
#=============================================================
#=============================================================
# are data axes the same?  ==================================
def check_axis(flist):
    flistlength = len(flist)
    if   flistlength == 0: return False
    elif flistlength == 1: return True
    elif flistlength > 1:
        ch_x = flist[0][3]['XUNI']
        for x in flist:
            if x[3]['XUNI'] != ch_x: return False
        if 'YUNI' in flist[0][3]:
            ch_y = flist[0][3]['YUNI']
            for x in flist:
                if 'YUNI' in x[3] and x[3]['YUNI'] != ch_y: return False
        else:
            for x in flist:
                if 'YUNI' in x[3]: return False
        return True
# set option values from values ==================================
def v_to_opt(value,file,isDTA):
    opt = {}
    y = 6 if isDTA == True else 3
    a = '' if isDTA == True else '@'
    if value['@c_black'] == True:
        opt['c'] = ['black'] * len(file)
    else:
        opt['c'] = []
        for x in range(len(file)):
            if file[x][y] != '':############################ 2D error
                opt['c'].append(file[x][y])
            else:
                try: opt['c'].append(COLORFUL[x])
                except: opt['c'].append('black')
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
    opt['grid'] = True if value[a+'@grid'] == True else False
    opt['t'] = True if value['@tight'] == True else False
    opt['mar_xr'] = -value['@mar_XR']/100
    opt['mar_xl'] = -value['@mar_XL']/100
    opt['mar_y'] = value['@mar_Ya']/100
    opt['y'] = False if value[a+'@noysc'] == True else True
    opt['stack'] = value['@stk']/100
    if 'Bottom' in value[a+'@cpos']: opt['posV'] = ['top',-1]
    else: opt['posV'] = ['bottom',1]
    if 'Right' in value[a+'@cpos']: opt['posH'] = ['right',-1,0.98,-1]
    else: opt['posH'] = ['left',1,0.02,0]
    if value[a+'@ctype'] == 'Spectrum': opt['ctyp'] = 'spectrum'
    else: opt['ctyp'] = 'list'
    if   value[a+'@csize'] == 'large': opt['csize'] = [18.0,0.015,0.08]
    elif value[a+'@csize'] == 'medium': opt['csize'] = [14.0,0.015,0.06]
    else: opt['csize'] = [10.0,0.015,0.04]
    opt['ax_size'] = 14.0 # temp
    
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
        if 'YNAM' in file[0][3]:
            opt['ylabel'] = f"{file[0][3]['YNAM']}"
        else: opt['ylabel'] = f"{file[0][3]['IRNAM']}"
        opt['xlabel'] = f"{file[0][3]['XNAM']} ({file[0][3]['XUNI']})"
        if file[0][5] & 1:
            opt['gfactor'] = True if value['@g_adjust'] == True else False
            opt['g_mod'] = float(value['@g_mod'])
            if value['@g_style'] == 'Bottom: MagField , Top: g-factor':
                opt['g_axis'], opt['g_field'] = 'Top', 'Bottom'
            elif value['@g_style'] == 'Bottom: g-factor , Top: MagField':
                opt['g_axis'], opt['g_field'] = 'Bottom', 'Top'
            else:
                opt['g_axis'], opt['g_field'] = 'Bottom', None
        else: opt['gfactor'],opt['g_mod'],opt['g_field'] = None,None,None
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
#        opt['column'] = int(value['@@column'])
        opt['gfactor'] = False
        opt['g_axis'], opt['g_field'] = None,None
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
# Normalize data ===============================================
def Normalize(dataR,param,opt,isDTA=True):
    if isDTA and opt['n'] == 'Normal': 
        if opt['nn'] & 8 and 'AVGS' in param: N = float(param['AVGS'])
        else: N = 1
        if opt['nn'] & 4 and 'SPTP' in param: CT = float(param['SPTP'])*1000
        else: CT = 1
        if opt['nn'] & 2 and 'RCAG' in param: G = 10**float(param['RCAG'])/20
        else: G = 1
        if opt['nn'] & 1 and 'MWPW' in param: P = float(param['MWPW'])*1000
        else: P = 1
        dataR = dataR / N / G / CT / (P*P)
    elif isDTA and opt['n'] == 'Ignore': # set max/ min = 1,-1 or 1,0
        if 'EXPT' in param and param['EXPT'] == 'CW':
            if param['XNAM'] == 'Field':
                ysize, base = 2, -1
            else: ysize, base = 1, 0
        else: ysize, base = 1, 0
        ymax,ymin = np.amax(dataR), np.amin(dataR)
        dataR = (dataR - ymin) / (ymax - ymin) *ysize +base
    elif isDTA == False and opt['n'] == 'Ignore': # set max/min = 1,-1
        ymax,ymin = np.amax(dataR), np.amin(dataR)
        dataR = (dataR - ymin) / (ymax - ymin) *2 -1
    else: None
    return dataR
# modified data list =====================================
def make_data_list(filelist,opt,isDTA=True):
    err = ''
    datalist, Datax,Datay, sa = [],[],[],[]
    for xfile in filelist:
        if isDTA == True:
            abs_x, _, Data_matrix, err_text, is_err = load_BES3T(xfile,opt)
#        abs_x, abs_y, Data_matrix, err_text, is_err = load_BES3T(xfile,opt)
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

"""
def make_data_list_2D(filelist,opt,isDTA=True):
    err = ''
    if isDTA == True:
        abs_x, abs_y, Data_matrix, err_text, is_err = load_BES3T(xfile,opt)
        if is_err == True: err += err_text
    return abs_x, abs_y, Data_matrix
"""
def get_xpos(xl,xwid,opt,DL):
    tx = xl[0]+xwid*opt['posH'][2]
    if opt['gfactor'] == True: # invert axis for g-factor
        if opt['posH'][0] == 'left':
            if DL[0][0] < tx: xpos = DL[0][0]
            else: xpos = tx
        elif opt['posH'][0] == 'right':
            if DL[0][-1] > tx: xpos = DL[0][-1]
            else: xpos = tx
    else:
        if opt['posH'][0] == 'left':
            if DL[0][0] > tx: xpos = DL[0][0] # if data is out of margin, shift caption inside
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
    if opt['gfactor'] == True:
        for w in range(len(DLc[0])):
            if xmin >= DLc[0][w] >= xmax:
                 newDL.append(DLc[1][w])
    else:
        for w in range(len(DLc[0])):
            if xmin <= DLc[0][w] <= xmax:
                 newDL.append(DLc[1][w])
    ypos = newDL[opt['posH'][1]]
    for y in newDL:
        if is_b and y > ypos: ypos = y
        if is_t and y < ypos: ypos = y
    return ypos + shifty

# show graph ============================================
# only for 1D data 
def graph_1D(file,value,isDTA):
    if isDTA == True and check_axis(file)==False: return 'All data must have the same XY axis. '
    opt = v_to_opt(value,file,isDTA)
    label_size = opt['csize'][0]
    try:
        DL, err = make_data_list(file,opt,isDTA)
        if err: return err
    except: return 'Data file cannot be read.'
    capt = make_captions(opt,file)
    if opt['gfactor'] == True and opt['g_axis'] == 'Top':
        fig, axf = plt.subplots(figsize=opt['size'],dpi=opt['dpi'])
        axf.set_ylabel(opt['ylabel'],fontsize=opt['ax_size'])
        axf.tick_params(labelsize=label_size)
        axf.xaxis.set_major_locator(ticker.MaxNLocator(6,steps=[1,2,2.5,5,10]))
        if opt['grid']==True: axf.grid(axis='y')
        ax = axf.twiny()
    else:
        fig, ax = plt.subplots(figsize=opt['size'],dpi=opt['dpi'])
    ax.set_xmargin(0)
    ax.set_ymargin(opt['mar_y'])
    ax.tick_params(labelsize=opt['ax_size'])
    plt.xlabel('',fontsize=opt['ax_size'])
    plt.ylabel('',fontsize=opt['ax_size'])
    if opt['grid']==True: ax.grid()
    if opt['y']==False: 
        ax.tick_params(labelleft=False)
        ax.tick_params(labelright=False)
        ax.set_yticks([])
    ax.set(ylabel=opt['ylabel'])
    ax.set(xlabel=opt['xlabel'])
    cnt = len(file)
    for c in range(cnt):
        ax.plot(DL[c][0], DL[c][1], color=opt['c'][c])
    xl, yl = ax.get_xlim(), ax.get_ylim()
    xwid, ywid= xl[1]-xl[0], yl[1]-yl[0]
    if opt['gfactor'] == True:
        ax.set_xlabel('g-factor')
        xl_l = xl[1]- xwid *opt['mar_xl']
        xl_r = xl[0]+ xwid *opt['mar_xr']
    else:
        xl_l = xl[0]+ xwid *opt['mar_xl']
        xl_r = xl[1]- xwid *opt['mar_xr']
    ax.set_xlim(xl_l,xl_r)
    xl, yl = ax.get_xlim(), ax.get_ylim()
    xwid, ywid= xl[1]-xl[0], yl[1]-yl[0]
    for c in range(cnt):
        if opt['ctyp'] == 'spectrum':
            xpos = get_xpos(xl,xwid,opt,DL[c])
            if opt['size'][0] < 5.5: tlength = xwid*opt['csize'][1]*len(capt[c])
            else: tlength = xwid*opt['csize'][1]*len(capt[c])
            ypos = get_ypos(DL[c],opt,tlength,ywid,xpos,xl)
        else: # list
            xpos = xl[0]+xwid*opt['posH'][2]
            if opt['posV'][0] == 'bottom':#upper
                ypos = yl[1]-opt['csize'][2]*ywid*(c+1)-ywid*0.03
            else:#down
                ypos = yl[0]+opt['csize'][2]*ywid*(cnt-c)+ywid*0.03
        ax.text(xpos, ypos,capt[c], ha=opt['posH'][0],va=opt['posV'][0],color=opt['c'][c],fontsize=label_size)
    if opt['size'][0] < 5.5:
        ax.xaxis.set_major_locator(ticker.MaxNLocator(6,steps=[1,2,2.5,5,10]))
    if opt['gfactor'] == True:
        ax.xaxis.set_major_locator(ticker.MaxNLocator(6))
    if opt['n'] == 'Normal': plt.title('** Normalized by parameters **')
    elif opt['n'] == 'Ignore': plt.title('** Normalized by max-min intensity **')
    if opt['gfactor'] == True:
        if opt['g_field'] == 'Top':
            axf = ax.twiny()
        if opt['g_field'] in ('Top','Bottom'):
            axf.set_xlabel(opt['xlabel'],fontsize=label_size)
            axf.tick_params(labelsize=label_size)
            mw = float(file[0][3]['MWFQ'])/1e9*714.418
            fl_left, fl_right = mw/xl[0], mw/xl[1]
            axf.set_xlim([fl_left,fl_right])
    if opt['t']==True: fig.tight_layout()
    plt.savefig('tmp',format='png')
    plt.close()
    return None
#=============================================================
# 2D data (1 file only)#####################################
def graph_2D(file,value,isDTA):
    xfile = file[0]
    opt = v_to_opt(value,file,isDTA)
    text_size = opt['csize'][0]
    if isDTA:
        abs_x, abs_y, Data_matrix, err_text, is_err = load_BES3T(xfile,opt)
    if is_err: return err
    fig, ax = plt.subplots(figsize=opt['size'],dpi=opt['dpi'])
    cs = ax.contourf(abs_x, abs_y, Data_matrix)
    xl, yl = ax.get_xlim(), ax.get_ylim()
    xl_l = xl[0]+(xl[1]-xl[0])*opt['mar_xl']
    xl_r = xl[1]-(xl[1]-xl[0])*opt['mar_xr']
    ax.set_xlim(xl_l,xl_r)
    ax.set_ymargin(opt['mar_y'])
    ax.tick_params(labelsize=text_size)
    plt.xlabel('',fontsize=text_size)
    plt.ylabel('',fontsize=text_size)
    if opt['gfactor']==True:
        if 'Field' in opt['xlabel']:
            axg = ax.twiny()
            xl = ax.get_xlim()
            axg.set_xlabel('g-factor',fontsize=text_size)
            axg.tick_params(labelsize=text_size)
            mw = float(xfile[3]['MWFQ'])/1e9*714.418
            fl_min, fl_max = mw/xl[0], mw/xl[1]
            axg.set_xlim([fl_min,fl_max])
            cbar = fig.colorbar(cs)
        if 'Field' in opt['ylabel']:
            axg = ax.twinx()
            yl = ax.get_ylim()
            axg.set_ylabel('g-factor',fontsize=text_size)
            axg.tick_params(labelsize=text_size)
            mw = float(xfile[3]['MWFQ'])/1e9*714.418
            fl_min, fl_max = mw/yl[0], mw/yl[1]
            axg.set_ylim([fl_min,fl_max])
            cbar = fig.colorbar(cs, pad=0.18)
    try: hoge = cbar
    except: cbar = fig.colorbar(cs)
    if opt['grid']==True: ax.grid()
    ax.set(ylabel=opt['ylabel'])
    ax.set(xlabel=opt['xlabel'])
    if opt['t']==True: fig.tight_layout()
    plt.savefig('tmp',format='png')
    plt.close()
    return None
#=============================================================
