import configparser
import os
import sys
import PySimpleGUI as sg

# Layout の作成と起動時に処理する関数たち

#外部テキストから設定を読み込み、なければ作成==============
#全体の設定
SETTING = configparser.ConfigParser()
setfile_name = 'setting.ini'

def save_ini_default():
    SETTING['DEFAULT'] = {
        'Initial_folder' : 'C:/Users',
        'File_list_row' : 8,
        'Data_list_row' : 5,
        'Light_mode' : False,
        'APP_good_DPI_mode' : False,
        'Window_Theme' : 'SandyBeach',
        'Color' : 'black,red,blue,limegreen,darkorange,magenta,deepskyblue,green,gray,blueviolet',
        'Figure_options' : 'DEFAULT',
        }
    SETTING['USER'] = {}
    with open('setting.ini','w') as f:
        SETTING.write(f)

if not os.path.exists(setfile_name):
    save_ini_default()
SETTING.read(setfile_name)
if 'USER' not in SETTING.sections():
    save_ini_default()

#作図のパラメータ
FIGURE_OPTIONS = configparser.ConfigParser()
figfile_name = 'figure_options.ini'

def save_ini_options():
    FIGURE_OPTIONS['DEFAULT'] = {
        'Figure_landscape' : True,
        'Figure_portrait' : False,
        'Figure_size_x' : 7,
        'Figure_size_y' : 5,
        'Figure_dpi' : 100,
        'Figure_tight' : False,
        'Color' : True,
        'Normalize_MWpower' : True,
        'Normalize_Gain' : True,
        'Normalize_CT' : True,
        'Normalize_Scans' : True,
        'DTA_Normalize' : 0,
        'DTA_noYscale' : True,
        'DTA_Grid' : True,
        'DTA_fixcolor' : False,
        'DTA_Captions' : 'Data name',
        'DTA_Csize' : 'medium',
        'DTA_Cpos1' : 'List',
        'DTA_Cpos2' : 'Top-Left'
        }
    with open(figfile_name, mode='w') as f:
        FIGURE_OPTIONS.write(f)

if not os.path.exists(figfile_name):
    save_ini_options()
FIGURE_OPTIONS.read(figfile_name)

#値の取得==================================================
ini_fo = SETTING.get('USER','Initial_folder')
file_row = SETTING.getint('USER','File_list_row')
data_row = SETTING.getint('USER','Data_list_row')
Light = SETTING.getboolean('USER','Light_mode')
DPI_mode = SETTING.getboolean('USER','APP_good_DPI_mode')
THEME = SETTING.get('USER','Window_Theme')
COLOR_TEXT = SETTING.get('USER','Color')
ini_figopt = SETTING.get('USER','Figure_options')

opt_fland = FIGURE_OPTIONS.getboolean(ini_figopt,'Figure_landscape')
opt_fport = FIGURE_OPTIONS.getboolean(ini_figopt,'Figure_portrait')
opt_fother = True if opt_fland == False and opt_fport == False else False
opt_fx = FIGURE_OPTIONS.getfloat(ini_figopt,'Figure_size_x')
opt_fy = FIGURE_OPTIONS.getfloat(ini_figopt,'Figure_size_y')
opt_dpi = FIGURE_OPTIONS.getfloat(ini_figopt,'Figure_dpi')
opt_tight = FIGURE_OPTIONS.getboolean(ini_figopt,'Figure_tight')
opt_color = FIGURE_OPTIONS.getboolean(ini_figopt,'Color')
opt_npower = FIGURE_OPTIONS.getboolean(ini_figopt,'Normalize_MWpower')
opt_ngain = FIGURE_OPTIONS.getboolean(ini_figopt,'Normalize_Gain')
opt_nct = FIGURE_OPTIONS.getboolean(ini_figopt,'Normalize_CT')
opt_nscans = FIGURE_OPTIONS.getboolean(ini_figopt,'Normalize_Scans')
opt_DTA_nig = True if FIGURE_OPTIONS.getboolean(ini_figopt,'DTA_Normalize') == 2 else False
opt_DTA_npar = True if FIGURE_OPTIONS.getboolean(ini_figopt,'DTA_Normalize') == 1 else False
opt_DTA_nnon = True if FIGURE_OPTIONS.getboolean(ini_figopt,'DTA_Normalize') == 0 else False
opt_DTA_noY = FIGURE_OPTIONS.getboolean(ini_figopt,'DTA_noYscale')
opt_DTA_Grid = FIGURE_OPTIONS.getboolean(ini_figopt,'DTA_Grid')
opt_DTA_fixcolor = FIGURE_OPTIONS.getboolean(ini_figopt,'DTA_fixcolor')
opt_DTA_Capt = FIGURE_OPTIONS.get(ini_figopt,'DTA_Captions')
opt_DTA_Csize = FIGURE_OPTIONS.get(ini_figopt,'DTA_Csize')
opt_DTA_Cpos1 = FIGURE_OPTIONS.get(ini_figopt,'DTA_Cpos1')
opt_DTA_Cpos2 = FIGURE_OPTIONS.get(ini_figopt,'DTA_Cpos2')

# 設定を保存する===========================================
def save_ini(value):
    SETTING['USER']['Initial_folder'] = str(value['@s_folder'])
    SETTING['USER']['File_list_row'] = str(value['@s_filerow'])
    SETTING['USER']['Data_list_row'] = str(value['@s_datarow'])
    SETTING['USER']['Light_mode'] = str(value['@s_light'])
    SETTING['USER']['APP_good_DPI_mode'] = str(value['@s_appDPI'])
    SETTING['USER']['Window_Theme'] = str(THEME)
    SETTING['USER']['Color'] = str(value['@c_edit'])
    with open('setting.ini', mode='w') as f:
        SETTING.write(f)

# GUIがぼやける現象を防ぐための関数========================
def make_dpi_aware():
  import ctypes
  import platform
  if int(platform.release()) >= 8:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
if DPI_mode:
    make_dpi_aware()

#定数などの設定============================================
nograph = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x02\xbc\x00\x00\x01\xf4\x08\x02\x00\x00\x00P;i\x88\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x0e\xc3\x00\x00\x0e\xc3\x01\xc7o\xa8d\x00\x00\r~IDATx^\xed\xdd\xdbu\xdb\xd6\x16@\xd1\xdby\xaaP\x15\xaaBM\xa8\t\x15\x91KR\x8c\xc5C\x82\xc4\x02Hdh\x04s~%6q\xb4\x01\x7f\xec\xa5\x87\xe9\xff\xfd\r\x00\x10\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x80[\x9f\xef\x7f\xfd\xf1\xf6\xf1u\xfeU`\xe7D\x03\xbb\xf3\xf5\xf1v\xde\x86\x7f,_\x8b\x97\x87\xfc\x17\x97\xaah\x00&\x88\x06vg"\x1a\xfe\xfa\xeb\xfd\xf3\xfc\xbb\x91h\xd8\xc6\xf0\x87\xb3\xf4\x0f\x05\xd8\x9ah`w&\xa3a\xe9\x86\x12\r\xdb\x10\r\xf0\xab\x89\x06v\xe7N4,\xdb\x8d\xa2a\x1b\xa2\x01~5\xd1\xc0\xee\xdc\x8b\x86E\xdbQ4lC4\xc0\xaf&\x1a\xd8\x9dq\xdf\x7f\\l\xc7\x05kJ4lC4\xc0\xaf&\x1a\xd8\x9d\xab}?\xac\xa9\xbc\xa8D\xc36D\x03\xfcj\xa2\x81\xdd\xb9\xd9\xf7c6\xb4\x15)\x1a\xb6!\x1a\xe0W\x13\r\xec\xce\xc4\xbe\xbf\\\x91mW\x89\x86m\x88\x06\xf8\xd5D\x03\xbb3\xb5\xef\x87]U\xb6\xd5\xdah\xf8\xfa\xfcx\x7f\x7f{\x1b>\xda\xe1\x7f\xdf\xde?>>\xff\xc5\xd5\xfc\xf9\xf11Nq\x1a\xe1\xf3\xeb\xcf\x089\x1a\xbe\xbe>?\x8f\xf7t<n\xbc\xad\xa3\xd3/\x9e\xee\xed\xf1\xcd]=\xffy\x13\x7fB\xaf\x99\x04xD4\xb0;\xd3\xfb~\\[\xb3\x1d\xb08\x1a\x8e\xb50\xbf\x18\xdf\xde7N\x87\xf91\xbeGH\xd10~\x81f\xd6)K\xce\x97^y6\x1a^7\t\xf0\x88h`w\xee\xed\xfbq\xf1\xcc\x94\xc0\xa2h\xf8\xfa\x0c\xbd\xf0#E\xc8\x1a}5\x0f\x9f\xa9\xbf*\x1aN\xa6\x0f\xfb\x97\xa3\xe1d\xb3\xc7\x0c\xffa\xa2\x81\xdd\xb9\xbf\xef\xc7\xd5\xf3\xf0{\x14=\x1a\x0e\xc5p~\xdd\x02\x87O\xf7\xcf\x97\xbf\xcc\xb2p\xb9\xf4\xd2h8xtoC=\xf4\x87\xb0\xc1$\xc0\x04\xd1\xc0\xee<\xd8\xf7W\x9f\xf0>\xd8)5\x1a\xaeN<\xf8\xfe\xd9\x81\xcb+\xbeN\xdf3\xb8y\xdd\xc3\x14Yhb\x8c\xef9\xce\xbf\x7ft\x18\xea\xf4\xa3\x0e\xe7\x17\xfcx\x18\r\x87s\x8e?)\xf0y\xbc\xa7\x9b\x1f\x178\xfe\xd2\xd4\xbd\xdd\x7f\xb0\xc3\xa0\xcb\xa2\xe1\xc5\x93\x00\x13D\x03\xbb\xf3p\xdf\x8f\xdb\xf5\xfe\xe2~x\xc8\x1fW\x9f\x00\xcf\xfc\xc4\xc2\xf5\xd7$^\x96\r\xd7\xc9\xf06\xf7\x1d\xfd\xf1\xfb)/\x98\xe3\xfa\x1b4ww\xf5\xcah\xe8\xf2$\xc0\x04\xd1\xc0\xee\xcc\xec\xfbqs\xdf[\x98%\x1a\xaevuZO\xe3G\x7f\xcdFkw4\xba\xbc\xe6\x05\xd1p0>\x8d{w\xb6y4\x1c\xb4I\x80\t\xa2\x81\xdd\x99\xdd\xf7eq\xcf\x1e\xb2z7\r\x1f\xfd\x05\x1bm\xdd\x18\xaf\x8f\x86q\x90{g\x0e/\xdaj\x9f\xa7I\x80\t\xa2\x81\xdd\xb9\\\x19\xd3\x1bc\xdc\xb3\x93\xbbk\xe1!K6\xd3p\xe1\xd3{s\xe5\x18\x1bDC:\xf3\xb57\x7f\xcf\x16w\x07\xbb \x1a\xd8\x9d\xf9}\x7f\xb5\xbb\xa6^5{\xc8\xcae}\xf4\xca\xc5\xb9v\x8c-\xd6\xea\xec3;x\xe5\xbd\xdfW&\x01&\x88\x06v\xa7m\x8c\xcb\xad9\xb1\xbef\x0fyf\xeb\xbepc\xaf=j\xfd\x08\xc7\xbf\xa6\xf0y\xfck\x18G\xa7\xf7a\xbc}{\xc6\xfbg\xbe2\x1a\x9e\x9b\x04\x98 \x1a\xd8\x9d\xf8i\xe6\xb0\xben\x16\xd8\xdc!O-\xbf\xd7m\xce\xd5\'-\x8b\x86\xe9\xbf\xce\xf8\xc8V\xd1\xf0\xbaI\x80\t\xa2\x81\xdd\x99\xdb\xf7\x7f\x0c\x0b\xec\xea\xa5s\x87<\xb5\xfc\x9e\xdd\x9c?V\x9fT\xa3\xe1\xfao0V\xf7\xce\\\x7f\xeb\xaf\x9e\x04\x98 \x1a\xd8\x9d\xb9}\x7f\xe1ru\x8e/\x9e;\xe4\xa9\xbd\xff\xd4\xc5\x83\x05\xf7:J\xd1pgM\x1f\xdfe\xe9\xfbm\x96\xbe\xdfg\xe9\xe0\xf4\xf22\xcc\xca[\xdf`\x12`\x82h`w\x16m\x8c1\x1b~\xb6\xd8\xdc!+\x97\xdf\xb7\xa7.\x1e\xac\xde\x8e\xf3\xd10\x0cyp\xf3\x0e\x937\xca0kn}\x9bI\x80\t\xa2\x81\xddY\xb61\xae6\xd2?{l\xee\x90\xe1\xb2\xdf\x11\r\x8bN\x9a\x8b\x86\xf1\xb1\xb4\x7f\x9cs\xee\x99\x1d-\x1fx\xabI\x80\t\xa2\x81\xddY\xba1\xae\xb6\xd2\xf7\x15\xb3\x87\xa4\xaf\xef\xdf\xf1\xcc\xb5\xa3a\xf6\x17F\xc3\xe5o\xe7s\xcb\x83_<\xf0f\x93\x00\x13D\x03\xbb\xb3|c\x0c\x8b\xe9\xfb\x9a\xd9C\x86\xed\xb7l1\xad\xda\x83w\xac=\xeb\xf2\xba\xdb\xe9\x17\xaf\xf6\x93\xf2\xe0\x97\x9e\xbc\xdd$\xc0\x04\xd1\xc0\xee\xac\xd9\x18c6\x1c\x96\xd3\xfc!\xc3:[\xb2\x99^\xd9\x0cs\xdb\xff\xae\xc7\x97\xad;\xb4<\xf8\xe1\xa9\x85\x9b\xdfn\x12`\x82h`wVm\x8ca\x99\x1d\xd6\xd9\xc7\xfc!\xe3%u\xfb\x8fW=\xbf\xd1\xd6M\xf1;\xa2!\x1c-\x1a\xe0_%\x1a\xd8\x9d\x95\x1bc\xdc\xbe\x97\xd2\x02l\x0b{\xc5%s\xc6#\xd3\r_Mq{\xcd\xf0\x82v\xe4\xe7\xdc\x99g\x97\x15\x10\x8e\xdep\x12\xe0\x96h`w.\xf7\xcc\xa2\x8d1\xec\xb3\x0b\xf7\x0f\xb9\xba\xe2\xf1\x8f\xf6_o\xb3\x97\xad\xb3\xeb)\x1e\x1d{3\xc4\xc1\xc4\x05\xe3\x91\x8f\x07=\xbdG\xe3\xf9\x95\x7f\xdc\xbd\xe4*Xf\xb3i\xbbI\x80[\xa2\x81\xddY\x1d\r\xd7\x0b\xed\x1f\x8f\x0e\xb9\r\x8d\xefw\x11\xb8\xbcb\xfa\xad\x8f_\xb8\xccn\xe7\xbe~+\x83\xc3@\xf7\xdf~yj\x92\xeb\xfbz\xbbys\x84\xf3\x91\xe7\xdf\xbfv\xff\xeen\x86=\xa6\xd6\xc5\xc9\xdf\xc7\xfe\xc4\xc4v\x93\x007D\x03\xbb\xb3>\x1a&6\xda\xd1\xe3C\xee\x94\xc6c\x17K\xf1%\x16\x0eq|#\xc5\xf3\x7f\x1eL\xdf\xdfm\x0e=v\xd8\xe5\x17\x8b\xfb\xd13+\'_>\x9f\xed&\x01\xae\x88\x06v\xe7\x99h\x98\xdcP\xb3\x87,\xfcg\x11\xb6Yc\xb5\x1b\xbe\xbf\x87ry\x9b\xf7\xe6\xc9wu\xfa\xdc\x7f\xc9\x83\x9f\xcf\x801\xaa\xb6\x9b\x04\x18\x88\x06v\xe7\xd9\x8dq\xb3\xd1\xd2!\x8f\xbeB\xfe\xe3\xb0\xd46\\as\xf1r\xf13\x17%\x1a\x0e\xbe\xe6n\xea\xbc\xa5\xcf/\xee\x0f~n\xd4\x9b\xaf\xc4l6\tpA4\xb0;Oo\x8c\xcb\x03\x8e\x16\x1cr\xfa\xee\xfa\xfb\xdb\xf8\xc3\x03\x87\xff=l\xb4\x9f\x95\xb6\xad\xf3O/\\L0\xf5\xd1c4\x9c\xdc\x1cx\xbc\xa3\x89\x1bZ\xfc\xe0o\x0f>\x9d|\xffYm6\t\xf0M4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00\x08\xfe\xfe\xfb\xff\x04Grj\xd3\x9e\xa2\x03\x00\x00\x00\x00IEND\xaeB`\x82'
I_yoko=30

CAPT = ['None','(Manual)','File name','Data name','Microwave Frequency','Microwave Power']
COLORFUL = [c for c in COLOR_TEXT.split(',') if c != '']
MAX_DATALIST = len(COLORFUL)

#レイアウト================================================
sg.theme(THEME)
DTA_col = sg.Tab(' DTA ',k='TAB_dta',layout=[[
    sg.Text('Folder',size=(5,1)), sg.InputText('',k='@fol_read',size=(I_yoko,1),enable_events=True),
    sg.FolderBrowse(initial_folder=ini_fo)],
    [sg.Text('Find:',size=(5,1)),
        sg.Combo(['1D'],default_value='1D',size=(4,1),k='@find_d',enable_events=True),
        sg.Combo(['all','Fieldsweep','Timescan','ENDOR',],default_value='all',k='@find_a',enable_events=True),
        sg.Combo(['all','CW','Pulse','Raw data','Manipulated',' (Free keyword) '],k='@find_m',size=(15,1),enable_events=True,
        tooltip=' After you input a FREE KEYWORD, please browse again or re-select the other finder box. ')],
    [sg.Listbox('',k='@liall',size=(I_yoko+15,file_row), select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED)],
    [sg.Button(' ↓ add '),sg.Button(' ↑ remove '),sg.Button('× Clear list')],
    [sg.Listbox('',k='@liuse',size=(I_yoko+10,data_row), select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED),
    sg.Frame('',relief='flat',layout=[[sg.Button(' ↑ ')],[sg.Button(' ↓ ')]])],
        [sg.Radio('Ignore Intensity',"tate",k='@same',default=opt_DTA_nig,enable_events=True),
        sg.Radio('Normalize',"tate",k='@normal',default=opt_DTA_npar,enable_events=True,
            tooltip=' EMX data are already normalized. \n Detail setting is in Option tab. '),
        sg.Radio('None',"tate",k='@no',default=opt_DTA_nnon,enable_events=True)],
    [sg.Checkbox('No Y scale',k='@noysc',default=opt_DTA_noY,enable_events=True),
    sg.Checkbox('Grid',k='@grid',default=opt_DTA_Grid,enable_events=True),
    sg.Radio('Fix Color',"fixcol",k='@fixcol',default=opt_DTA_fixcolor,enable_events=True,
    tooltip=' Colors are fixed to the spectrum when you chenge the order. '),
    sg.Radio('Forget Color',"fixcol",k='@fogcol',default=not opt_DTA_fixcolor,enable_events=True)],
    [sg.Text('Separate (%)',size=(10,1)),sg.Slider(k='@stk',range=(0,120),size=(25,10),default_value=0,orientation='h',enable_events=True)],
    [sg.Text('X Margin (%)',size=(10,1)),sg.Slider(k='@mar',range=(5,-30),size=(25,10),default_value=5,orientation='h',enable_events=True)],
    [sg.Text('Captions'),
    sg.Combo(CAPT,k='@capt',default_value=opt_DTA_Capt,enable_events=True),
    sg.Text('size'),
    sg.Combo(['large','medium','small'],k='@csize',size=(8,1),default_value=opt_DTA_Csize,enable_events=True)],
    [sg.InputText('1;2;3;(manual captions)',k='@capt_my',size=(I_yoko+18,1))],
    [sg.Text('position'),sg.Combo(['List','Spectrum'],k='@ctype',default_value=opt_DTA_Cpos1,enable_events=True),
    sg.Combo(['Top-Right','Top-Left','Bottom-Right','Bottom-Left'],k='@cpos',default_value=opt_DTA_Cpos2,enable_events=True),
#    sg.Checkbox('align',k='@calign'),
    ],
    ])

DAT_col = sg.Tab(' dat ',k='TAB_dat',layout=[[
    sg.Text('Folder',size=(5,1)),sg.InputText('',k='@@fol_read',size=(I_yoko,1),enable_events=True),
    sg.FolderBrowse(initial_folder=ini_fo)],
    [sg.Text('Mode',size=(4,1)),sg.Combo(['1D'],size=(8,1),default_value='1D',k='@@mode',enable_events=True),
    sg.Text('Keyword',size=(6,1)),sg.InputText('',k='@@find_free',size=(20,1),enable_events=True,tooltip=' you can search for multiple words by separating with a space. ')],
    [sg.Listbox('',k='@@liall',size=(I_yoko+15,file_row), select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED)],
    [sg.Button(' ↓ add ',k='@@b_add'),sg.Button(' ↑ remove ',k='@@b_remove'),sg.Button('× Clear list',k='@@b_clear')],
    [sg.Listbox('',k='@@liuse',size=(I_yoko+10,data_row), select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED),
    sg.Frame('',relief='flat',layout=[[sg.Button(' ↑ ',k='@@b_up')],[sg.Button(' ↓ ',k='@@b_down')]])],
    [sg.Radio('Ignore Intensity',"Dtate",k='@@same',enable_events=True),
        sg.Radio('Do not Normalize',"Dtate",k='@@no',default=True,enable_events=True)],
    [sg.Checkbox('No Y scale',k='@@noysc',default=True,enable_events=True),
        sg.Checkbox('Grid',k='@@grid',default=True,enable_events=True),
    sg.Radio('Fix Color',"fixcold",k='@@fixcol',enable_events=True,
    tooltip=' Colors are fixed to the spectrum when you chenge the order. '),
    sg.Radio('Forget Color',"fixcold",k='@@fogcol',default=True,enable_events=True)],
    [sg.Text('Separate (%)',size=(10,1)),sg.Slider(k='@@stk',range=(0,120),size=(25,10),default_value=0,orientation='h',enable_events=True)],
    [sg.Text('X Margin (%)',size=(10,1)),sg.Slider(k='@@mar',range=(5,-30),size=(25,10),default_value=5,orientation='h',enable_events=True)],
    [sg.Text('Captions'),sg.Combo(['None','File name','(Manual)'],k='@@capt',default_value='File name',enable_events=True),
    sg.Text('size'),sg.Combo(['large','medium','small'],k='@@csize',size=(8,1),default_value='medium',enable_events=True)],
    [sg.InputText('1;2;3;(manual captions)',k='@@capt_my',size=(I_yoko+18,1))],
    [sg.Text('position'),sg.Combo(['List','Spectrum'],k='@@ctype',default_value='List',enable_events=True),
    sg.Combo(['Top-Right','Top-Left','Bottom-Right','Bottom-Left'],k='@@cpos',default_value='Top-Left',enable_events=True),
#    sg.Checkbox('align',k='@@calign'),
    ],
    [sg.Text('X name'),sg.Combo(['None','Magnetic field (G)','Time (ns)','Time (μs)','Distance (nm)','Radio frequency (MHz)','(write here)'],k='@@xnam',size=(13,1),enable_events=True),
     sg.Text('Y name'),sg.Combo(['None','Intensity','Magnetic field (G)','Time (s)','(write here)'],k='@@ynam',size=(13,1),enable_events=True)],
    ])

cal_col = sg.Tab(' Data Calculation ',k='TAB_cal',layout=[
#    [sg.Text('Data Calculation Option')],
    [sg.Frame(' Normalize ',layout=[
    [sg.Text('Caution: EMX data are already normalized.')],
#        [sg.Radio('EMX',"NOR",k='@n_emx',enable_events=True),
#        sg.Radio('Other (E500, E580, E680, etc.)',"NOR",k='@n_other',default=True,enable_events=True)],
        [sg.Checkbox('MW power',k='@n_power',default=opt_npower,enable_events=True),
        sg.Checkbox('Gain',k='@n_gain',default=opt_ngain,enable_events=True)],
        [sg.Checkbox('Conversion Time',k='@n_convtime',default=opt_nct,enable_events=True),
        sg.Checkbox('Number of Scans',k='@n_scans',default=opt_nscans,enable_events=True),],
        [sg.Text('Intensity = Intensity\n / Scans / 10^(Gain /20) / ConvTime[sec] / Power[W] ^2',k='@n_text')],
    ])],
#    [sg.Frame(' g-factor (for DTA data only)',layout=[
#        [sg.Checkbox('Show g-factor axis',k='@g_cal'),
#        sg.Text('Modify:'),sg.InputText('0',k='@g_mod',size=(5,1)),sg.Text('G')],
#        [sg.Text('g-factor \n= MWfreq[GHz] / (MagneticField + Modify[G]) *714.418')],
#        [sg.Radio('Adjust spectra to g-factor axis',"gfactor",k='@g_adjustg',default=True)],
#        [sg.Radio('Adjust spectra to magnetic field axis',"gfactor",k='@g_adjustm')],
#        [sg.Checkbox('Hide magnetic field axis',k='@g_hidemag')],
#    ])],
    ])

fig_col = sg.Tab(' Figure Option ',k='TAB_adv',layout=[
    [sg.Text('')],
    [sg.Frame(' Figure size ',layout=[
    [sg.Radio('7:5 landscape',"size",k='@size_yoko',default=opt_fland,enable_events=True),
        sg.Radio('5:7 portrait',"size",k='@size_tate',default=opt_fport,enable_events=True)],
        [sg.Radio('Other',"size",k='@size_manual',default=opt_fother,enable_events=True),
        sg.InputText(opt_fx,k='@size_MX',size=(5,1),enable_events=True),sg.Text('x'),
        sg.InputText(opt_fy,k='@size_MY',size=(5,1),enable_events=True),
        sg.Text('  DPI '),sg.InputText(opt_dpi,k='@size_dpi',size=(6,1),enable_events=True),],
        [sg.Checkbox('Tight figure',k='@tight',default=opt_tight,enable_events=True)],
    ])],
    [sg.Frame(' Color ',layout=[
    [sg.Radio('Black all',"color",k='@c_black',default=not opt_color,enable_events=True),
     sg.Radio('Colorful',"color",k='@c_color',default=opt_color,enable_events=True)],
    [sg.Text(' The Color order can be changed in Setting Tab.')],
#            [sg.InputText(COLORFUL[0],size=(7,1)),sg.InputText(COLORFUL[1],size=(7,1)),sg.InputText(COLORFUL[2],size=(7,1)),sg.InputText(COLORFUL[3],size=(7,1)),sg.InputText(COLORFUL[4],size=(7,1))],
#            [sg.InputText(COLORFUL[5],size=(7,1)),sg.InputText(COLORFUL[6],size=(7,1)),sg.InputText(COLORFUL[7],size=(7,1)),sg.InputText(COLORFUL[8],size=(7,1)),sg.InputText(COLORFUL[9],size=(7,1))],
    ])],
    [sg.Frame(' Expansion ',layout=[
        [sg.Text('X Margin (%)',size=(10,1)),sg.Slider(k='@mar_Xa',range=(5,-30),size=(25,10),default_value=5,orientation='h',enable_events=True)],
        [sg.Text('Left (%)',size=(7,1)),sg.Slider(k='@mar_XL',range=(0,45),size=(9,10),default_value=0,orientation='h',enable_events=True),
        sg.Text('Right (%)',size=(8,1)),sg.Slider(k='@mar_XR',range=(45,0),size=(9,10),default_value=0,orientation='h',enable_events=True)],
        [sg.Text('Y Margin (%)',size=(10,1)),sg.Slider(k='@mar_Ya',range=(10,-40),size=(25,10),default_value=5,orientation='h',enable_events=True)],
    ])],
    ])

set_col = sg.Tab(' Setting ',k='TAB_set',layout=[
    [sg.Text('Initial folder for browse:')],
    [sg.InputText(ini_fo,size=(I_yoko+11,2),k='@s_folder')],
    [sg.FolderBrowse(initial_folder=ini_fo,target=(-1,-1))],
    [sg.Text('')],
    [sg.Text('File list row length:',size=(20,1)),
    sg.InputText(file_row,size=(5,1),k='@s_filerow'),sg.Text('default: 8')],
    [sg.Text('Data list row length:',size=(20,1)),
    sg.InputText(data_row,size=(5,1),k='@s_datarow'),sg.Text('default: 5')],
    [sg.Checkbox('Light mode ON',k='@s_light',default=Light)],
    [sg.Checkbox('Disable blurry effect (for Windows)',k='@s_appDPI',default=DPI_mode)],
    [sg.Text('')],
    [sg.Text('Edit color set:     '),sg.Button('reset')],
    [sg.Text('Number of the list equals to the capacity of the graph.')],
    [sg.Multiline(COLOR_TEXT,k='@c_edit',size=(45,2))],
    [sg.Text('Available color? See:')],
    [sg.InputText('https://matplotlib.org/3.3.3/gallery/color/named_colors.html',size=(49,1))],
    [sg.Text('')],
    [sg.Button('save settings')]
    ])

migi_col = sg.Frame('',relief='flat',layout=[
    [sg.Button('show'),sg.Button('save figure'),
    sg.Checkbox('Light mode',k='@light',default=Light,
    tooltip=' In Light mode, Press "show" to show graph. '),],
#    sg.Text('   Figure setting:'),
#    sg.Combo(['(default)'],k='@optionlist',size=(15,1),enable_events=True),
#    sg.Button('save this',tooltip=' Save current figure options and data calculation options. ')],
    [sg.Image(data=nograph,k='@imgraph')],
    ])

Opt_col = sg.Tab(' Option ',k='TAB_opt',layout=[
    [sg.TabGroup([[cal_col],[fig_col]])],
    ])

How_col = sg.Tab(' How to ',k='TAB_how',layout=[
    [sg.Text('\n1. Add data file(s) to the list. \n\n\
2. A graph is displayed.\n In Light mode, press "show" button to show the graph.\n\n\
3. Set options under the list or in the Option tab. \n\n\
4. The figure can be saved as a PNG file. \n\n\
 Before you move to the dat/DTA Tab, clear the data list.')]
    ])



LAYOUT = [[sg.TabGroup([[DTA_col],[DAT_col],[Opt_col],[set_col],[How_col]]), migi_col]]

