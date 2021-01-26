"""
ESR quick graphing ver 1.05 (2021/01/26)
functions for loading data and graphing
"""
import math
import os
import sys
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
def __load_BES3T(file_info,opt):
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
                for j, x in enumerate(abscissa[i]):
                    jiba = x + opt['g_mod']
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
        if opt['imag']:
            Data_matrix = Data_matrix.imag
        else:
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
def __load_dat(file_info,opt):
    fullname = file_info[2] + '/' + file_info[1]
    try: allLines = np.loadtxt(fullname)
    except:
        try: allLines = np.loadtxt(fullname, delimiter = ',')
        except: return None, None, f'{file_info[1]} cannot be read.\n'
    if len(np.shape(allLines)) == 1:# no x axis --> add index
        L = len(allLines)
        abs_x = np.linspace(1,L,L)
        data_r = allLines
    else:
        abs_x = allLines[:,0]
        if opt['column'] == 1:
            data_r = allLines[:,1]
        elif opt['column'] < (col_size := len(allLines[0])) + 1:
            data_r = allLines.T[1:opt['column']+1]
        else:
            data_r = allLines.T[1:col_size]
    return abs_x, data_r, None
#=============================================================
#=============================================================
# are data axes the same?  ==================================
def __check_axis(flist):
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
def __v_to_opt(value,file,isDTA):
    opt = {}
    num_file = len(file)
    y = 6 if isDTA == True else 3
    a = '' if isDTA == True else '@'
    if value['@c_black'] == True:
        opt['c'] = ['black'] * num_file
        opt['ls'] = ['-', '--', ':', '-,'] * 5
    else:
        opt['c'] = []
        for i, xfile in enumerate(file):
            if xfile[y] != '':############################ 2D error
                opt['c'].append(xfile[y])
            else:
                try: opt['c'].append(COLORFUL[i])
                except: opt['c'].append('black')
        opt['ls'] = ['-'] * num_file
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
#    opt['mar_y'] = value['@mar_Ya']/100
    opt['mar_yh'] = value['@mar_YH']/100
    opt['mar_yl'] = value['@mar_YL']/100
    opt['y'] = False if value[a+'@noysc'] == True else True
    opt['stack'] = value['@stk']/100
#    if 'Bottom' in value[a+'@cpos']: opt['posV'] = ['top',-1,0]
    if 'Lower' in value[a+'@cpos'] or 'Bottom' in value[a+'@cpos']: opt['posV'] = ['top',-1,0]
    else: opt['posV'] = ['bottom',1,-1]
    if 'Right' in value[a+'@cpos']: opt['posH'] = ['right',-1,0.98,-1]
    else: opt['posH'] = ['left',1,0.02,0]
    if value[a+'@ctype'] == 'Spectrum': opt['ctyp'] = 'spectrum'
    else: opt['ctyp'] = 'list'
    if   value[a+'@csize'] == 'large': opt['csize'] = 18.0
    elif value[a+'@csize'] == 'medium': opt['csize'] = 14.0
    else: opt['csize'] = 10.0
    opt['ax_size'] = 14.0 # temp
    
    if isDTA == True:
        if   value['@normal'] == True:
            opt['n'] = 'Normal'
            opt['nn'] = ''
            if value['@n_power'] == True: opt['nn'] += 'P'
            if value['@n_gain'] == True: opt['nn'] += 'G'
            if value['@n_timeconst'] == True: opt['nn'] += 'T'
            if value['@n_scans'] == True: opt['nn'] += 'N'
            if value['@n_Q'] == True: opt['nn'] += 'Q'
        elif value['@same'] == True: opt['n'] = 'Ignore'
        else: opt['n'] = 'None'
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
        if value['@imag'] == True: opt['imag'] = True
        else: opt['imag'] = False
    else:# dat
        if value['@@same'] == True: opt['n'] = 'Ignore'
        else: opt['n'] = 'None'
        opt['xlabel'] = value['@@xnam'] if value['@@xnam'] != 'None' else ''
        opt['ylabel'] = value['@@ynam'] if value['@@ynam'] != 'None' else ''
        opt['column'] = int(value['@@column'])
        opt['gfactor'] = False
        opt['g_axis'], opt['g_field'] = None,None
    return opt

def __make_captions(value,isDTA,file_list):
    if isDTA == True:
        if value['@capt'] == 'File name':
            capt = [x[0] for x in file_list]
        elif value['@capt'] == 'Data name':
            capt = [x[3]['TITL'] for x in file_list]
        elif value['@capt'] == 'Microwave Frequency':
            capt = [x[3]['FrequencyMon'] for x in file_list]
        elif value['@capt'] == 'Microwave Power':
            capt = [x[3]['Power'] for x in file_list]
        elif value['@capt'] == '(Manual)':
            capt = value['@capt_my'].split(';')
            if len(capt)<len(file_list):
                for i in range(len(file_list)-len(capt)):
                    capt.append('')
        else: capt = [''] * len(file_list)
    elif isDTA == False:
        if value['@@capt'] == 'File name':
            capt = [x[0] for x in file_list]
        elif value['@@capt'] == '(Manual)':
            capt = value['@@capt_my'].split(';')
            if len(capt)<len(file_list):
                for i in range(len(file_list)-len(capt)):
                    capt.append('')
        else: capt = [''] * len(file_list)
    else: capt = [''] * len(file_list)
    return capt

# Normalize data ===============================================
def __Normalize(dataR,param,opt,isDTA=True):
    if isDTA and opt['n'] == 'Normal': 
        if 'N' in opt['nn'] and 'AVGS' in param: N = float(param['AVGS'])
        else: N = 1
        if 'T' in opt['nn'] and 'RCTC' in param: TC = float(param['RCTC'])*1000
        else: TC = 1
        if 'G' in opt['nn'] and 'RCAG' in param: G = 10**(float(param['RCAG'])/20)
        else: G = 1
        if 'P' in opt['nn'] and 'MWPW' in param: P = float(param['MWPW'])*1000
        else: P = 1
        if 'Q' in opt['nn'] and 'QValue' in param: Q = float(param['QValue'])
        else: Q = 1
        dataR /= (N * G * TC * P**0.5 * Q)
    elif isDTA and opt['n'] == 'Ignore': # set max/ min = 1,-1 or 1,0
        if 'EXPT' in param and param['EXPT'] == 'CW' and param['XNAM'] == 'Field':
              ysize, base = 2, -1
        else: ysize, base = 1, 0
        ymax,ymin = np.amax(dataR), np.amin(dataR)
#        dataR = (dataR - ymin) / (ymax - ymin) *ysize +base
        dataR -= ymin
        dataR /= (ymax - ymin) *ysize
        dataR += base
    elif isDTA == False and opt['n'] == 'Ignore': # set max/min = 1,-1
        ymax,ymin = np.amax(dataR), np.amin(dataR)
#        dataR = (dataR - ymin) / (ymax - ymin) *2 -1
        dataR -= ymin
        dataR /= (ymax - ymin) *2
        dataR -= 1
    else: pass
    return dataR
# modified data list =====================================
def __make_data_list(filelist,opt,isDTA=True):
    err = ''
    Datax, Datay, sa = [],[],[]
    for xfile in filelist:
        if isDTA == True:
            abs_x, _, Data_matrix, err_text, is_err = __load_BES3T(xfile,opt)
            if is_err == True: err += err_text
            if opt['imag'] == True and Data_matrix[0].imag:
                tmp_y = __Normalize(Data_matrix.imag, xfile[3],opt,True)
            else:
                tmp_y = __Normalize(Data_matrix.real, xfile[3],opt,True)
            sa.append(np.amax(tmp_y)-np.amin(tmp_y))
        else:
            abs_x, Data_matrix, err_text = __load_dat(xfile,opt)
            if err_text: return None,err_text
            if len(dim := np.shape(Data_matrix)) == 2:
                for i, col in enumerate(Data_matrix):
                    col = __Normalize(col,None,opt,False)
                    if i == 0: tmp_y = col
                    else: tmp_y = np.vstack([tmp_y, col])
                    sa.append(np.amax(col)-np.amin(col))
            else:
                tmp_y = __Normalize(Data_matrix,None,opt,False)
                sa.append(np.amax(tmp_y)-np.amin(tmp_y))
        Datay.append(tmp_y)
        Datax.append(abs_x)
#        sa.append(np.amax(tmp_y) - np.amin(tmp_y))
    maxheight = max(sa)* opt['stack']
    for c, y in enumerate(Datay):
        y -= maxheight * c
    return Datax, Datay, err

def __get_capt_position(DXc,DYc,opt,tlength,xwid,ywid,xl):
    xlimit = xl[0]+xwid*opt['posH'][2]
    yfloat = opt['posV'][1]*ywid*0.02
    if opt['gfactor'] == True: # invert xaxis for g-factor
        if opt['posH'][0] == 'left':
            if DXc[0] < xlimit + tlength:
                  xpos = DXc[0] - tlength
            else: xpos = xlimit
            text_area_y = [y for i, y in enumerate(DYc) if xpos > DXc[i] > xpos + tlength]
        elif opt['posH'][0] == 'right':
            if DXc[-1] > xlimit - tlength:
                  xpos = DXc[-1] + tlength
            else: xpos = xlimit
            text_area_y = [y for i, y in enumerate(DYc) if xpos - tlength > DXc[i] > xpos]
    else:
        if opt['posH'][0] == 'left':
            if DXc[0] > xlimit + tlength:
                  xpos = DXc[0] - tlength
            else: xpos = xlimit
            if len(np.shape(DYc)) == 1:
                text_area_y = [y for i, y in enumerate(DYc) if xpos < DXc[i] < xpos + tlength]
            else:
                text_area_y = [y for DYcc in DYc 
                                 for i, y in enumerate(DYcc) if xpos < DXc[i] < xpos + tlength]
        elif opt['posH'][0] == 'right':
            if DXc[-1] < xlimit - tlength:
                  xpos = DXc[-1] + tlength
            else: xpos = xlimit
            if len(np.shape(DYc)) == 1:
                text_area_y = [y for i, y in enumerate(DYc) if xpos - tlength < DXc[i] < xpos]
            else:
                text_area_y = [y for DYcc in DYc 
                                 for i, y in enumerate(DYcc) if xpos - tlength < DXc[i] < xpos]
    if text_area_y == []:
        ypos = DYc[opt['posH'][3]] + yfloat
    else:
        text_area_y.sort()# min: 0 max : -1
        ypos = text_area_y[opt['posV'][2]] + yfloat
    return xpos, ypos

# show graph ============================================
# only for 1D data 
def graph_1D(file,value,isDTA):
    if isDTA == True and __check_axis(file)==False: return 'All data must have the same XY axis. '
    opt = __v_to_opt(value,file,isDTA)
    label_size = opt['csize']
    try:
        DX, DY, err = __make_data_list(file,opt,isDTA)
        if err: return err
    except: return 'Data file cannot be read.'
    capt = __make_captions(value,isDTA,file)
    if opt['gfactor'] == True and opt['g_axis'] == 'Top':
        fig, axf = plt.subplots(figsize=opt['size'],dpi=opt['dpi'])
        axf.set_ylabel(opt['ylabel'],fontsize=opt['ax_size'])
        axf.tick_params(labelsize=opt['ax_size'])
        axf.xaxis.set_major_locator(ticker.MaxNLocator(6,steps=[1,2,2.5,5,10]))
        if opt['grid']==True: axf.grid(axis='y')
        ax = axf.twiny()
    else:
        fig, ax = plt.subplots(figsize=opt['size'],dpi=opt['dpi'])
    ax.set_xmargin(0)
#    ax.set_ymargin(opt['mar_y'])
    ax.set_ymargin(0)
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
    if isDTA == False and opt['column'] > 1:
        for c in range(cnt):
            if len(np.shape(DY[c])) > 1:
                for i in range(np.shape(DY[c])[0]):
                    ax.plot(DX[c], DY[c][i], color=COLORFUL[i])
                opt['c'] = ['black'] * cnt
            else: ax.plot(DX[c], DY[c], color=opt['c'][c])
    else:
        for c in range(cnt):
            ax.plot(DX[c], DY[c], color=opt['c'][c])
    xl, yl = ax.get_xlim(), ax.get_ylim()
    xwid, ywid= xl[1]-xl[0], yl[1]-yl[0]
    if opt['gfactor'] == True:
        ax.set_xlabel('g-factor')
        xl_l = xl[1]- xwid *opt['mar_xl']
        xl_r = xl[0]+ xwid *opt['mar_xr']
    else:
        xl_l = xl[0]+ xwid *opt['mar_xl']
        xl_r = xl[1]- xwid *opt['mar_xr']
    yl_l = yl[0]- ywid *opt['mar_yl']
    yl_h = yl[1]+ ywid *opt['mar_yh']
    ax.set_xlim(xl_l,xl_r)
    ax.set_ylim(yl_l,yl_h)
    xl, yl = ax.get_xlim(), ax.get_ylim()
    xwid, ywid= xl[1]-xl[0], yl[1]-yl[0]
    for c in range(cnt):
        if opt['ctyp'] == 'spectrum':
            tlength = xwid *opt['csize']*len(capt[c])*0.0125/opt['size'][0]
            xpos, ypos = __get_capt_position(DX[c],DY[c],opt,tlength,xwid,ywid,xl)
        else: # list
            xpos = xl[0]+xwid*opt['posH'][2]
            if opt['posV'][0] == 'bottom':#upper
                ypos = yl[1]-ywid*(0.02+opt['csize']*(c+1)*0.022/opt['size'][1])
            else:#down
                ypos = yl[0]+ywid*(0.02+opt['csize']*(cnt-c)*0.022/opt['size'][1])
        ax.text(xpos, ypos, capt[c], ha=opt['posH'][0], va=opt['posV'][0], color=opt['c'][c], fontsize=label_size)
    if opt['size'][0] < 6:
        ax.xaxis.set_major_locator(ticker.MaxNLocator(6,steps=[1,2,2.5,5,10]))
    if opt['gfactor'] == True:
        ax.xaxis.set_major_locator(ticker.MaxNLocator(6))
    if opt['n'] == 'Normal': plt.title('** Normalized by parameters **')
    elif opt['n'] == 'Ignore': plt.title('** Normalized by max-min intensity **')
    if opt['gfactor'] == True:
        if opt['g_field'] == 'Top':
            axf = ax.twiny()
        if opt['g_field'] in ('Top','Bottom'):
            axf.set_xlabel(opt['xlabel'],fontsize=opt['ax_size'])
            axf.tick_params(labelsize=opt['ax_size'])
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
    opt = __v_to_opt(value,file,isDTA)
    text_size = opt['csize']
    if isDTA:
        abs_x, abs_y, Data_matrix, err_text, is_err = __load_BES3T(xfile,opt)
    if is_err: return err
    fig, ax = plt.subplots(figsize=opt['size'],dpi=opt['dpi'])
    cs = ax.contourf(abs_x, abs_y, Data_matrix)
    xl, yl = ax.get_xlim(), ax.get_ylim()
    xl_l = xl[0]+(xl[1]-xl[0])*opt['mar_xl']
    xl_r = xl[1]-(xl[1]-xl[0])*opt['mar_xr']
    yl_l = yl[0]-(yl[1]-yl[0])*opt['mar_yl']
    yl_h = yl[1]+(yl[1]-yl[0])*opt['mar_yh']
    ax.set_xlim(xl_l,xl_r)
    ax.set_ylim(yl_l,yl_h)
#    ax.set_ymargin(opt['mar_y'])
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
    try: _ = cbar # cbar exist
    except: cbar = fig.colorbar(cs)
    if opt['grid']==True: ax.grid()
    ax.set(ylabel=opt['ylabel'])
    ax.set(xlabel=opt['xlabel'])
    if opt['t']==True: fig.tight_layout()
    plt.savefig('tmp',format='png')
    plt.close()
    return None
#=============================================================
