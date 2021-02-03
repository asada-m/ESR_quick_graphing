"""
ESR quick graphing ver 1.06 (2021/02/03)
Layout and functions for initializing
"""
import configparser
import os
#import sys
import PySimpleGUI as sg

APP_TITLE = 'ESR quick graphing  ver.1.06'

# read setting file and create if it is not existing ===========
SETTING = configparser.ConfigParser()
SETTING_default = configparser.ConfigParser()
setfile_name = 'setting.ini'
SETTING_default['DEFAULT'] = {
    'Initial_folder' : 'C:/Users',
    'File_list_row' : 8,
    'Data_list_row' : 5,
    'Light_mode' : False,
    'APP_good_DPI_mode' : False,
    'Window_Theme' : 'SandyBeach',
    'Color' : 'black,red,blue,limegreen,darkorange,magenta,deepskyblue,green,gray,blueviolet',
    'Figure_options' : 'DEFAULT',
    }

if os.path.exists(setfile_name):
    SETTING.read(setfile_name)
    for x in SETTING_default['DEFAULT'].keys():
        if x not in SETTING['DEFAULT'].keys():
            SETTING['DEFAULT'][x] = SETTING_default['DEFAULT'][x]
    if 'USER' not in SETTING.sections():
        SETTING['USER'] = {}
    with open(setfile_name,'w') as f:
        SETTING.write(f)
else:
    SETTING['DEFAULT'] = SETTING_default['DEFAULT']
    SETTING['USER'] = {}
    with open(setfile_name,'w') as f:
        SETTING.write(f)
    SETTING.read(setfile_name)

# figure parameters
FIGURE_OPTIONS = configparser.ConfigParser()
FIGURE_OPTIONS_default = configparser.ConfigParser()
figfile_name = 'figure_options.ini'
fo = {}
FIGURE_OPTIONS_default['DEFAULT'] = {
        'Figure_landscape' : True,
        'Figure_portrait' : False,
        'Figure_size_x' : 7.0,
        'Figure_size_y' : 5.0,
        'Figure_dpi' : 100.0,
        'Figure_tight' : False,
        'Color' : True,
        'Normalize_MWpower' : True,
        'Normalize_Gain' : True,
        'Normalize_TC' : True,
        'Normalize_Scans' : True,
        'Normalize_Qvalue' : True,
        'DTA_Normalize' : 0,
        'DTA_noYscale' : True,
        'DTA_Grid' : True,
        'DTA_fixcolor' : False,
        'DTA_Captions' : 'Data name',
        'DTA_Csize' : 'medium',
        'DTA_Cpos1' : 'List',
        'DTA_Cpos2' : 'Upper-Left',
        'dat_Normalize' : 0,
        'dat_noYscale' : True,
        'dat_Grid' : True,
        'dat_fixcolor' : False,
        'dat_Captions' : 'File name',
        'dat_Csize' : 'medium',
        'dat_Cpos1' : 'List',
        'dat_Cpos2' : 'Upper-Left',
        'dat_Xname' : '',
        'dat_Yname' : '',
        'g-factor' : False,
        'Field_Modification' : 0,
        'Axis_style' : 'Bottom: MagField , Top: g-factor',
        'Imaginary' : False,
        }

if os.path.exists(figfile_name):
    FIGURE_OPTIONS.read(figfile_name)
    for x in FIGURE_OPTIONS_default['DEFAULT'].keys():
        if x not in FIGURE_OPTIONS['DEFAULT'].keys():
            FIGURE_OPTIONS['DEFAULT'][x] = FIGURE_OPTIONS_default['DEFAULT'][x]
    with open(figfile_name,'w') as f:
        FIGURE_OPTIONS.write(f)
else:
    FIGURE_OPTIONS['DEFAULT'] = FIGURE_OPTIONS_default['DEFAULT']
    with open(figfile_name,'w') as f:
        FIGURE_OPTIONS.write(f)
    FIGURE_OPTIONS.read(figfile_name)

# getting values ==================================================
ini_fo = SETTING.get('USER','Initial_folder')
file_row = SETTING.getint('USER','File_list_row')
data_row = SETTING.getint('USER','Data_list_row')
Light = SETTING.getboolean('USER','Light_mode')
DPI_mode = SETTING.getboolean('USER','APP_good_DPI_mode')
THEME = SETTING.get('USER','Window_Theme')
COLOR_TEXT = SETTING.get('USER','Color')
if SETTING.get('USER','Figure_options') in FIGURE_OPTIONS.sections():
    ini_figopt = SETTING.get('USER','Figure_options')
else: ini_figopt = 'DEFAULT'

def load_options_fromfile(section):
    fo['@size_yoko'] = FIGURE_OPTIONS.getboolean(section,'Figure_landscape')
    fo['@size_tate'] = FIGURE_OPTIONS.getboolean(section,'Figure_portrait')
    fo['@size_manual'] = True if fo['@size_yoko'] == False and fo['@size_tate'] == False else False
    fo['@size_MX'] = FIGURE_OPTIONS.getfloat(section,'Figure_size_x')
    fo['@size_MY'] = FIGURE_OPTIONS.getfloat(section,'Figure_size_y')
    fo['@size_dpi'] = FIGURE_OPTIONS.getfloat(section,'Figure_dpi')
    fo['@tight'] = FIGURE_OPTIONS.getboolean(section,'Figure_tight')
    fo['@c_color'] = FIGURE_OPTIONS.getboolean(section,'Color')
    fo['@c_black'] = not fo['@c_color']
    fo['@n_power'] = FIGURE_OPTIONS.getboolean(section,'Normalize_MWpower')
    fo['@n_gain'] = FIGURE_OPTIONS.getboolean(section,'Normalize_Gain')
    fo['@n_timeconst'] = FIGURE_OPTIONS.getboolean(section,'Normalize_TC')
    fo['@n_scans'] = FIGURE_OPTIONS.getboolean(section,'Normalize_Scans')
    fo['@n_Q'] = FIGURE_OPTIONS.getboolean(section,'Normalize_Qvalue')
    fo['@same'] = True if FIGURE_OPTIONS.getint(section,'DTA_Normalize') == 2 else False
    fo['@normal'] = True if FIGURE_OPTIONS.getint(section,'DTA_Normalize') == 1 else False
    fo['@no'] = True if FIGURE_OPTIONS.getint(section,'DTA_Normalize') == 0 else False
    fo['@noysc'] = FIGURE_OPTIONS.getboolean(section,'DTA_noYscale')
    fo['@grid'] = FIGURE_OPTIONS.getboolean(section,'DTA_Grid')
    fo['@fixcol'] = FIGURE_OPTIONS.getboolean(section,'DTA_fixcolor')
    fo['@fogcol'] = not fo['@fixcol']
    fo['@capt'] = FIGURE_OPTIONS.get(section,'DTA_Captions')
    fo['@csize'] = FIGURE_OPTIONS.get(section,'DTA_Csize')
    fo['@ctype'] = FIGURE_OPTIONS.get(section,'DTA_Cpos1')
    fo['@cpos'] = FIGURE_OPTIONS.get(section,'DTA_Cpos2')
    fo['@@same'] = True if FIGURE_OPTIONS.getint(section,'dat_Normalize') == 1 else False
    fo['@@no'] = True if FIGURE_OPTIONS.getint(section,'dat_Normalize') == 0 else False
    fo['@@noysc'] = FIGURE_OPTIONS.getboolean(section,'dat_noYscale')
    fo['@@grid'] = FIGURE_OPTIONS.getboolean(section,'dat_Grid')
    fo['@@fixcol'] = FIGURE_OPTIONS.getboolean(section,'dat_fixcolor')
    fo['@@fogcol'] = not fo['@@fixcol']
    fo['@@capt'] = FIGURE_OPTIONS.get(section,'dat_Captions')
    fo['@@csize'] = FIGURE_OPTIONS.get(section,'dat_Csize')
    fo['@@ctype'] = FIGURE_OPTIONS.get(section,'dat_Cpos1')
    fo['@@cpos'] = FIGURE_OPTIONS.get(section,'dat_Cpos2')
    fo['@@xnam'] = FIGURE_OPTIONS.get(section,'dat_Xname')
    fo['@@ynam'] = FIGURE_OPTIONS.get(section,'dat_Yname')
    fo['@g_adjust'] = FIGURE_OPTIONS.getboolean(section,'g-factor')
    fo['@g_mod'] = FIGURE_OPTIONS.getfloat(section,'Field_Modification')
    fo['@g_style'] = FIGURE_OPTIONS.get(section,'Axis_style')
    fo['@imag'] = FIGURE_OPTIONS.getboolean(section,'Imaginary')

load_options_fromfile(ini_figopt)

def update_options(window,value):
    section = value['@opt_load_name']
    if section not in ['DEFAULT'] + FIGURE_OPTIONS.sections(): return False
    load_options_fromfile(section)
    namelist = ('@size_yoko','@size_tate','@size_manual','@tight','@c_color','@c_black',
    '@n_power','@n_gain','@n_timeconst','@n_scans','@n_Q','@same','@normal','@no','@noysc','@grid','@fixcol','@fogcol',
    '@@same','@@no','@@noysc','@@grid','@@fixcol','@@fogcol','@size_MX','@size_MY','@size_dpi',
    '@capt','@csize','@ctype','@cpos','@@capt','@@csize','@@ctype','@@cpos','@@xnam','@@ynam',
    '@g_adjust','@g_mod','@g_style','@imag',)
    for x in namelist:
        window[x].update(value = fo[x])
        value[x] = fo[x]
    sg.popup(f'" {section} " option values are loaded.')
    return True

# save settings in file ===========================================
def save_ini(value):
    SETTING['USER']['Initial_folder'] = value['@s_folder']
    SETTING['USER']['File_list_row'] = str(int(value['@s_filerow']))
    SETTING['USER']['Data_list_row'] = str(int(value['@s_datarow']))
    SETTING['USER']['Light_mode'] = str(value['@s_light'])
    SETTING['USER']['APP_good_DPI_mode'] = str(value['@s_appDPI'])
    if value['@s_theme'] in sg.theme_list():
        SETTING['USER']['Window_Theme'] = value['@s_theme']
    else: SETTING['USER']['Window_Theme'] = THEME
    SETTING['USER']['Color'] = value['@c_edit']
    SETTING['USER']['Figure_options'] = value['@ini_figopt']########
    with open('setting.ini', mode='w') as f:
        SETTING.write(f)

def save_options_pop(name,value):
    if name.upper() == 'DEFAULT':
        sg.popup(f'The name " {name} " is inhibited.')
        return False
    if name in FIGURE_OPTIONS.sections():
        ov = sg.popup_ok_cancel(f'" {name} " already exists.\n\nOverWrite ?')
        if ov != 'OK':
            return False
    FIGURE_OPTIONS[name] = {}
    FIGURE_OPTIONS[name]['Figure_landscape'] = str(value['@size_yoko'])
    FIGURE_OPTIONS[name]['Figure_portrait'] = str(value['@size_tate'])
    FIGURE_OPTIONS[name]['Figure_size_x'] = str(value['@size_MX'])
    FIGURE_OPTIONS[name]['Figure_size_y'] = str(value['@size_MY'])
    FIGURE_OPTIONS[name]['Figure_dpi'] = str(value['@size_dpi'])
    FIGURE_OPTIONS[name]['Figure_tight'] = str(value['@tight'])
    FIGURE_OPTIONS[name]['Color'] = str(value['@c_color'])
    FIGURE_OPTIONS[name]['Normalize_MWpower'] = str(value['@n_power'])
    FIGURE_OPTIONS[name]['Normalize_Gain'] = str(value['@n_gain'])
    FIGURE_OPTIONS[name]['Normalize_TC'] = str(value['@n_timeconst'])
    FIGURE_OPTIONS[name]['Normalize_Scans'] = str(value['@n_scans'])
    FIGURE_OPTIONS[name]['Normalize_Qvalue'] = str(value['@n_Q'])
    if value['@same'] == True: FIGURE_OPTIONS[name]['DTA_Normalize'] = '2'
    elif value['@normal'] == True: FIGURE_OPTIONS[name]['DTA_Normalize'] = '1'
    else: FIGURE_OPTIONS[name]['DTA_Normalize'] = '0'
    FIGURE_OPTIONS[name]['DTA_noYscale'] = str(value['@noysc'])
    FIGURE_OPTIONS[name]['DTA_Grid'] = str(value['@grid'])
    FIGURE_OPTIONS[name]['DTA_fixcolor'] = str(value['@fixcol'])
    FIGURE_OPTIONS[name]['DTA_Captions'] = str(value['@capt'])
    FIGURE_OPTIONS[name]['DTA_Csize'] = str(value['@csize'])
    FIGURE_OPTIONS[name]['DTA_Cpos1'] = str(value['@ctype'])
    FIGURE_OPTIONS[name]['DTA_Cpos2'] = str(value['@cpos'])
    FIGURE_OPTIONS[name]['dat_Normalize'] = '1' if value['@@same'] == True else '0'
    FIGURE_OPTIONS[name]['dat_noYscale'] = str(value['@@noysc'])
    FIGURE_OPTIONS[name]['dat_Grid'] = str(value['@@grid'])
    FIGURE_OPTIONS[name]['dat_fixcolor'] = str(value['@@fixcol'])
    FIGURE_OPTIONS[name]['dat_Captions'] = str(value['@@capt'])
    FIGURE_OPTIONS[name]['dat_Csize'] = str(value['@@csize'])
    FIGURE_OPTIONS[name]['dat_Cpos1'] = str(value['@@ctype'])
    FIGURE_OPTIONS[name]['dat_Cpos2'] = str(value['@@cpos'])
    FIGURE_OPTIONS[name]['dat_Xname'] = str(value['@@xnam'])
    FIGURE_OPTIONS[name]['dat_Yname'] = str(value['@@ynam'])
    FIGURE_OPTIONS[name]['g-factor'] = str(value['@g_adjust'])
    FIGURE_OPTIONS[name]['Field_Modification'] = str(value['@g_mod'])
    FIGURE_OPTIONS[name]['Axis_style'] = str(value['@g_style'])
    FIGURE_OPTIONS[name]['Imaginary'] = str(value['@imag'])
    with open(figfile_name,'w') as f:
        FIGURE_OPTIONS.write(f)
    sg.popup(f'" {name} " saved.')
    return True

def delete_option(section):
    if section.upper() == 'DEFAULT':
        sg.popup('" DEFAULT " cannot be deleted !')
        return
    sOK = sg.popup_ok_cancel(f'Delete " {section} " option set. \n\nReally ?')
    if sOK != 'OK': return
    FIGURE_OPTIONS.remove_section(section)
    with open(figfile_name,'w') as f:
        FIGURE_OPTIONS.write(f)
    sg.popup(f'" {section} " deleted.')

# function to fix blurry effect ========================
def make_dpi_aware():
  import ctypes
  import platform
  if platform.system() == 'Windows' and int(platform.release()) >= 8:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)

if DPI_mode:
    make_dpi_aware()

# setting parameters ============================================
nograph = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x02\xbc\x00\x00\x01\xf4\x08\x02\x00\x00\x00P;i\x88\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x0e\xc3\x00\x00\x0e\xc3\x01\xc7o\xa8d\x00\x00\r~IDATx^\xed\xdd\xdbu\xdb\xd6\x16@\xd1\xdby\xaaP\x15\xaaBM\xa8\t\x15\x91KR\x8c\xc5C\x82\xc4\x02Hdh\x04s~%6q\xb4\x01\x7f\xec\xa5\x87\xe9\xff\xfd\r\x00\x10\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x80[\x9f\xef\x7f\xfd\xf1\xf6\xf1u\xfeU`\xe7D\x03\xbb\xf3\xf5\xf1v\xde\x86\x7f,_\x8b\x97\x87\xfc\x17\x97\xaah\x00&\x88\x06vg"\x1a\xfe\xfa\xeb\xfd\xf3\xfc\xbb\x91h\xd8\xc6\xf0\x87\xb3\xf4\x0f\x05\xd8\x9ah`w&\xa3a\xe9\x86\x12\r\xdb\x10\r\xf0\xab\x89\x06v\xe7N4,\xdb\x8d\xa2a\x1b\xa2\x01~5\xd1\xc0\xee\xdc\x8b\x86E\xdbQ4lC4\xc0\xaf&\x1a\xd8\x9dq\xdf\x7f\\l\xc7\x05kJ4lC4\xc0\xaf&\x1a\xd8\x9d\xab}?\xac\xa9\xbc\xa8D\xc36D\x03\xfcj\xa2\x81\xdd\xb9\xd9\xf7c6\xb4\x15)\x1a\xb6!\x1a\xe0W\x13\r\xec\xce\xc4\xbe\xbf\\\x91mW\x89\x86m\x88\x06\xf8\xd5D\x03\xbb3\xb5\xef\x87]U\xb6\xd5\xdah\xf8\xfa\xfcx\x7f\x7f{\x1b>\xda\xe1\x7f\xdf\xde?>>\xff\xc5\xd5\xfc\xf9\xf11Nq\x1a\xe1\xf3\xeb\xcf\x089\x1a\xbe\xbe>?\x8f\xf7t<n\xbc\xad\xa3\xd3/\x9e\xee\xed\xf1\xcd]=\xffy\x13\x7fB\xaf\x99\x04xD4\xb0;\xd3\xfb~\\[\xb3\x1d\xb08\x1a\x8e\xb50\xbf\x18\xdf\xde7N\x87\xf91\xbeGH\xd10~\x81f\xd6)K\xce\x97^y6\x1a^7\t\xf0\x88h`w\xee\xed\xfbq\xf1\xcc\x94\xc0\xa2h\xf8\xfa\x0c\xbd\xf0#E\xc8\x1a}5\x0f\x9f\xa9\xbf*\x1aN\xa6\x0f\xfb\x97\xa3\xe1d\xb3\xc7\x0c\xffa\xa2\x81\xdd\xb9\xbf\xef\xc7\xd5\xf3\xf0{\x14=\x1a\x0e\xc5p~\xdd\x02\x87O\xf7\xcf\x97\xbf\xcc\xb2p\xb9\xf4\xd2h8xtoC=\xf4\x87\xb0\xc1$\xc0\x04\xd1\xc0\xee<\xd8\xf7W\x9f\xf0>\xd8)5\x1a\xaeN<\xf8\xfe\xd9\x81\xcb+\xbeN\xdf3\xb8y\xdd\xc3\x14Yhb\x8c\xef9\xce\xbf\x7ft\x18\xea\xf4\xa3\x0e\xe7\x17\xfcx\x18\r\x87s\x8e?)\xf0y\xbc\xa7\x9b\x1f\x178\xfe\xd2\xd4\xbd\xdd\x7f\xb0\xc3\xa0\xcb\xa2\xe1\xc5\x93\x00\x13D\x03\xbb\xf3p\xdf\x8f\xdb\xf5\xfe\xe2~x\xc8\x1fW\x9f\x00\xcf\xfc\xc4\xc2\xf5\xd7$^\x96\r\xd7\xc9\xf06\xf7\x1d\xfd\xf1\xfb)/\x98\xe3\xfa\x1b4ww\xf5\xcah\xe8\xf2$\xc0\x04\xd1\xc0\xee\xcc\xec\xfbqs\xdf[\x98%\x1a\xaevuZO\xe3G\x7f\xcdFkw4\xba\xbc\xe6\x05\xd1p0>\x8d{w\xb6y4\x1c\xb4I\x80\t\xa2\x81\xdd\x99\xdd\xf7eq\xcf\x1e\xb2z7\r\x1f\xfd\x05\x1bm\xdd\x18\xaf\x8f\x86q\x90{g\x0e/\xdaj\x9f\xa7I\x80\t\xa2\x81\xdd\xb9\\\x19\xd3\x1bc\xdc\xb3\x93\xbbk\xe1!K6\xd3p\xe1\xd3{s\xe5\x18\x1bDC:\xf3\xb57\x7f\xcf\x16w\x07\xbb \x1a\xd8\x9d\xf9}\x7f\xb5\xbb\xa6^5{\xc8\xcae}\xf4\xca\xc5\xb9v\x8c-\xd6\xea\xec3;x\xe5\xbd\xdfW&\x01&\x88\x06v\xa7m\x8c\xcb\xad9\xb1\xbef\x0fyf\xeb\xbepc\xaf=j\xfd\x08\xc7\xbf\xa6\xf0y\xfck\x18G\xa7\xf7a\xbc}{\xc6\xfbg\xbe2\x1a\x9e\x9b\x04\x98 \x1a\xd8\x9d\xf8i\xe6\xb0\xben\x16\xd8\xdc!O-\xbf\xd7m\xce\xd5\'-\x8b\x86\xe9\xbf\xce\xf8\xc8V\xd1\xf0\xbaI\x80\t\xa2\x81\xdd\x99\xdb\xf7\x7f\x0c\x0b\xec\xea\xa5s\x87<\xb5\xfc\x9e\xdd\x9c?V\x9fT\xa3\xe1\xfao0V\xf7\xce\\\x7f\xeb\xaf\x9e\x04\x98 \x1a\xd8\x9d\xb9}\x7f\xe1ru\x8e/\x9e;\xe4\xa9\xbd\xff\xd4\xc5\x83\x05\xf7:J\xd1pgM\x1f\xdfe\xe9\xfbm\x96\xbe\xdfg\xe9\xe0\xf4\xf22\xcc\xca[\xdf`\x12`\x82h`w\x16m\x8c1\x1b~\xb6\xd8\xdc!+\x97\xdf\xb7\xa7.\x1e\xac\xde\x8e\xf3\xd10\x0cyp\xf3\x0e\x937\xca0kn}\x9bI\x80\t\xa2\x81\xddY\xb61\xae6\xd2?{l\xee\x90\xe1\xb2\xdf\x11\r\x8bN\x9a\x8b\x86\xf1\xb1\xb4\x7f\x9cs\xee\x99\x1d-\x1fx\xabI\x80\t\xa2\x81\xddY\xba1\xae\xb6\xd2\xf7\x15\xb3\x87\xa4\xaf\xef\xdf\xf1\xcc\xb5\xa3a\xf6\x17F\xc3\xe5o\xe7s\xcb\x83_<\xf0f\x93\x00\x13D\x03\xbb\xb3|c\x0c\x8b\xe9\xfb\x9a\xd9C\x86\xed\xb7l1\xad\xda\x83w\xac=\xeb\xf2\xba\xdb\xe9\x17\xaf\xf6\x93\xf2\xe0\x97\x9e\xbc\xdd$\xc0\x04\xd1\xc0\xee\xac\xd9\x18c6\x1c\x96\xd3\xfc!\xc3:[\xb2\x99^\xd9\x0cs\xdb\xff\xae\xc7\x97\xad;\xb4<\xf8\xe1\xa9\x85\x9b\xdfn\x12`\x82h`wVm\x8ca\x99\x1d\xd6\xd9\xc7\xfc!\xe3%u\xfb\x8fW=\xbf\xd1\xd6M\xf1;\xa2!\x1c-\x1a\xe0_%\x1a\xd8\x9d\x95\x1bc\xdc\xbe\x97\xd2\x02l\x0b{\xc5%s\xc6#\xd3\r_Mq{\xcd\xf0\x82v\xe4\xe7\xdc\x99g\x97\x15\x10\x8e\xdep\x12\xe0\x96h`w.\xf7\xcc\xa2\x8d1\xec\xb3\x0b\xf7\x0f\xb9\xba\xe2\xf1\x8f\xf6_o\xb3\x97\xad\xb3\xeb)\x1e\x1d{3\xc4\xc1\xc4\x05\xe3\x91\x8f\x07=\xbdG\xe3\xf9\x95\x7f\xdc\xbd\xe4*Xf\xb3i\xbbI\x80[\xa2\x81\xddY\x1d\r\xd7\x0b\xed\x1f\x8f\x0e\xb9\r\x8d\xefw\x11\xb8\xbcb\xfa\xad\x8f_\xb8\xccn\xe7\xbe~+\x83\xc3@\xf7\xdf~yj\x92\xeb\xfbz\xbbys\x84\xf3\x91\xe7\xdf\xbfv\xff\xeen\x86=\xa6\xd6\xc5\xc9\xdf\xc7\xfe\xc4\xc4v\x93\x007D\x03\xbb\xb3>\x1a&6\xda\xd1\xe3C\xee\x94\xc6c\x17K\xf1%\x16\x0eq|#\xc5\xf3\x7f\x1eL\xdf\xdfm\x0e=v\xd8\xe5\x17\x8b\xfb\xd13+\'_>\x9f\xed&\x01\xae\x88\x06v\xe7\x99h\x98\xdcP\xb3\x87,\xfcg\x11\xb6Yc\xb5\x1b\xbe\xbf\x87ry\x9b\xf7\xe6\xc9wu\xfa\xdc\x7f\xc9\x83\x9f\xcf\x801\xaa\xb6\x9b\x04\x18\x88\x06v\xe7\xd9\x8dq\xb3\xd1\xd2!\x8f\xbeB\xfe\xe3\xb0\xd46\\as\xf1r\xf13\x17%\x1a\x0e\xbe\xe6n\xea\xbc\xa5\xcf/\xee\x0f~n\xd4\x9b\xaf\xc4l6\tpA4\xb0;Oo\x8c\xcb\x03\x8e\x16\x1cr\xfa\xee\xfa\xfb\xdb\xf8\xc3\x03\x87\xff=l\xb4\x9f\x95\xb6\xad\xf3O/\\L0\xf5\xd1c4\x9c\xdc\x1cx\xbc\xa3\x89\x1bZ\xfc\xe0o\x0f>\x9d|\xffYm6\t\xf0M4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00HD\x03\x00\x90\x88\x06\x00 \x11\r\x00@"\x1a\x00\x80D4\x00\x00\x89h\x00\x00\x12\xd1\x00\x00$\xa2\x01\x00\x08\xfe\xfe\xfb\xff\x04Grj\xd3\x9e\xa2\x03\x00\x00\x00\x00IEND\xaeB`\x82'
I_yoko=30

CAPT = ['None','(Manual)','File name','Data name','Microwave Frequency','Microwave Power','(other DSC keys)']
COLORFUL = [c for c in COLOR_TEXT.split(',') if c != '']
MAX_DATALIST = 20 #temp

# layout ================================================
sg.theme(THEME)
if sg.theme_text_color() == '1234567890' or sg.theme_background_color == '1234567890':
    white_bcolor=None
else:
    white_bcolor=(sg.theme_text_color(),sg.theme_background_color())

DTA_col = sg.Tab(' DTA ',k='TAB_dta',layout=[[
    sg.InputText('C:/',k='@fol_read',size=(I_yoko+9,1),enable_events=True),
#    sg.FolderBrowse(k='@fol_browse',initial_folder=ini_fo)],
    sg.Button('Browse',k='@fol_browse')],
    [sg.Text('Find:'),
        sg.Combo(['1D','2D'],default_value='1D',size=(4,1),k='@find_d',enable_events=True),
        sg.Combo(['all','Fieldsweep','Timescan','ENDOR',],default_value='all',k='@find_a',enable_events=True),
        sg.Combo(['all','CW','Pulse','Raw data','Manipulated',' (Keyword: input here) '],k='@find_m',size=(18,1),enable_events=True,
        tooltip=' After you input a KEYWORD, please browse again or re-select the other finder box. ')],
    [sg.Listbox('',k='@liall',size=(I_yoko+15,file_row), select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED,bind_return_key=True)],
    [sg.Button(' ↓ add '),sg.Button(' ↑ remove '),sg.Button('× Clear list'),
    sg.Text('  '),sg.Button('parameter',button_color=white_bcolor),
    ],
    [sg.Listbox('',k='@liuse',size=(I_yoko+10,data_row), select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED,bind_return_key=True),
    sg.Frame('',relief='flat',layout=[[sg.Button(' ↑ ',pad=(0,3))],[sg.Button(' ↓ ',pad=(0,3))]])],
        [sg.Radio('Ignore Intensity',"tate",k='@same',default=fo['@same'],enable_events=True),
        sg.Radio('Normalize',"tate",k='@normal',default=fo['@normal'],enable_events=True,
            tooltip=' EMX data are already normalized. \n Detail setting is in Option tab. '),
        sg.Radio('None',"tate",k='@no',default=fo['@no'],enable_events=True)],
    [sg.Checkbox('align in g-factor → see Option Tab',k='@g_adjust',default=fo['@g_adjust'],enable_events=True,pad=(3,0)),
    sg.Checkbox('Imaginary',k='@imag',default=False,enable_events=True,pad=(3,0))
    ],
    [sg.Checkbox('No Y scale',k='@noysc',default=fo['@noysc'],enable_events=True),
    sg.Checkbox('Grid',k='@grid',default=fo['@grid'],enable_events=True),
    sg.Radio('Fix color',"fixcol",k='@fixcol',pad=(3,0),default=fo['@fixcol'],enable_events=True,
    tooltip=' Colors are fixed to the spectrum when you chenge the order. '),
    sg.Radio('Reset color',"fixcol",k='@fogcol',pad=(3,0),default=fo['@fogcol'],enable_events=True)],
    [sg.Text('Captions'),
    sg.Combo(CAPT,k='@capt',default_value=fo['@capt'],enable_events=True),
    sg.Text('size'),
    sg.Combo(['large','medium','small'],k='@csize',size=(8,1),default_value=fo['@csize'],enable_events=True)],
    [sg.InputText('1;2;3;(manual captions)',k='@capt_my',size=(I_yoko+18,1))],
    [sg.Text('position'),sg.Combo(['List','Spectrum'],k='@ctype',default_value=fo['@ctype'],enable_events=True),
    sg.Combo(['Upper-Left','Upper-Right','Lower-Left','Lower-Right'],k='@cpos',default_value=fo['@cpos'],enable_events=True),
    sg.Checkbox('align',k='@c_align',visible=False),
    ],
#    sg.Frame('',relief='groove',pad=(0,0),size=(15,1),layout=[
#    [sg.Text('Slice:',k='@2D_text',visible=True),
#    sg.Spin(list(range(1,11)),k='@2D_slice',size=(3,1),visible=True)]])
    ])

DAT_col = sg.Tab(' dat ',k='TAB_dat',layout=[[
    sg.InputText('C:/',k='@@fol_read',size=(I_yoko+9,1),enable_events=True),
#    sg.FolderBrowse(k='@@fol_browse',initial_folder=ini_fo)],
    sg.Button('Browse',k='@@fol_browse')],
    [sg.Text('Mode'),sg.Combo(['1D'],size=(3,1),default_value='1D',k='@@mode',enable_events=True),
    sg.Text('Col'),sg.Spin(list(range(1,21)),k='@@column',size=(3,1)),
    sg.Text('Find'),sg.InputText('',k='@@find_free',size=(17,1),enable_events=True,
    tooltip=' if separated with a space, multiple words can be searched. ')],
    [sg.Listbox('',k='@@liall',size=(I_yoko+15,file_row), select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED,bind_return_key=True)],
    [sg.Button(' ↓ add ',k='@@b_add'),sg.Button(' ↑ remove ',k='@@b_remove'),sg.Button('× Clear list',k='@@b_clear'),
    ],
    [sg.Listbox('',k='@@liuse',size=(I_yoko+10,data_row), select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED,bind_return_key=True),
    sg.Frame('',relief='flat',layout=[[sg.Button(' ↑ ',k='@@b_up',pad=(0,3))],[sg.Button(' ↓ ',k='@@b_down',pad=(0,3))]])],
    [sg.Radio('Ignore Intensity',"Dtate",k='@@same',default=fo['@@same'],enable_events=True),
        sg.Radio('Do not Normalize',"Dtate",k='@@no',default=fo['@@no'],enable_events=True)],
    [sg.Checkbox('No Y scale',k='@@noysc',default=fo['@@noysc'],enable_events=True),
        sg.Checkbox('Grid',k='@@grid',default=fo['@@grid'],enable_events=True),
    sg.Radio('Fix color',"fixcold",k='@@fixcol',pad=(3,0),default=fo['@@fixcol'],enable_events=True,
    tooltip=' Colors are fixed to the spectrum when you chenge the order. '),
    sg.Radio('Reset color',"fixcold",k='@@fogcol',pad=(3,0),default=fo['@@fogcol'],enable_events=True)],
    [sg.Text('Captions'),sg.Combo(['None','File name','(Manual)'],k='@@capt',default_value=fo['@@capt'],enable_events=True),
    sg.Text('size'),sg.Combo(['large','medium','small'],k='@@csize',size=(8,1),default_value=fo['@@csize'],enable_events=True)],
    [sg.InputText('1;2;3;(manual captions)',k='@@capt_my',size=(I_yoko+18,1))],
    [sg.Text('position'),sg.Combo(['List','Spectrum'],k='@@ctype',default_value=fo['@@ctype'],enable_events=True),
    sg.Combo(['Upper-Left','Upper-Right','Lower-Left','Lower-Right'],k='@@cpos',default_value=fo['@@cpos'],enable_events=True),
#    sg.Button('memo',k='@@b_memo',button_color=white_bcolor),
    ],
    [sg.Text('X name',pad=((3,1),3)),
    sg.Combo(['None','Magnetic field (G)','Time (ns)','Time (μs)','Distance (nm)','Radio frequency (MHz)','(write here)'],k='@@xnam',size=(13,1),default_value=fo['@@xnam'],enable_events=True),
     sg.Text('Y name',pad=((3,1),3)),
     sg.Combo(['None','Intensity','Magnetic field (G)','Time (s)','(write here)'],k='@@ynam',size=(13,1),default_value=fo['@@ynam'],enable_events=True)],
    ])

Opt_col = sg.Tab(' Option ',k='TAB_opt',layout=[
    [sg.Frame(' Normalize (for DTA data)',layout=[
    [sg.Text('Caution: EMX normalizes spectra automatically.')],
#        [sg.Radio('EMX',"NOR",k='@n_emx',enable_events=True),
#        sg.Radio('Other (E500, E580, E680, etc.)',"NOR",k='@n_other',default=True,enable_events=True)],
        [sg.Checkbox('MW power',k='@n_power',default=fo['@n_power'],pad=(5,0),enable_events=True),
        sg.Checkbox('Gain',k='@n_gain',default=fo['@n_gain'],pad=(5,0),enable_events=True),
        sg.Checkbox('Q-value',k='@n_Q',default=fo['@n_Q'],enable_events=True),],
        [sg.Checkbox('TimeConstant',k='@n_timeconst',default=fo['@n_timeconst'],pad=(5,0),enable_events=True),
        sg.Checkbox('Number of Scans',k='@n_scans',default=fo['@n_scans'],pad=(5,0),enable_events=True),],
        [sg.Text('Intensity = Intensity\n / Scans / 10^(Gain /20) / TimeConst[s] / √Power[W] / Q',k='@n_text')],
    ])],
    [sg.Frame(' g-factor (for DTA data)',layout=[
        [sg.Text('Field Modification:'),sg.InputText(fo['@g_mod'],k='@g_mod',size=(5,1),enable_events=True),sg.Text('G')],
        [sg.Text('g-factor \n= MWfreq[GHz] / (MagneticField + Modify[G]) *714.418')],
        [sg.Text('X axis style:'),
        sg.Combo(['Bottom: g-factor , Top: MagField','Bottom: g-factor , Top: none','Bottom: MagField , Top: g-factor'],
            k='@g_style',size=(32,1),default_value=fo['@g_style'],enable_events=True,
            tooltip=' When spectra are aligned in g-factor, \n Magnetic field of the 1st data in the list will be shown. ')],
    ])],
#    [sg.Frame(' Axis transformation',layout=[
#        [sg.Checkbox('Gauss --> mT')],
#        [sg.Checkbox('ns --> μs')],
#        [sg.Checkbox('ns --> ms')],
#        [sg.Checkbox('nm --> Angstrom')]
#    ])],
    [sg.Frame(' Figure size ',layout=[
    [sg.Radio('7:5 landscape',"size",k='@size_yoko',default=fo['@size_yoko'],enable_events=True),
        sg.Radio('5:7 portrait',"size",k='@size_tate',default=fo['@size_tate'],enable_events=True)],
        [sg.Radio('Other',"size",k='@size_manual',default=fo['@size_manual'],enable_events=True),
        sg.InputText(fo['@size_MX'],k='@size_MX',size=(5,1),enable_events=True),sg.Text('x'),
        sg.InputText(fo['@size_MY'],k='@size_MY',size=(5,1),enable_events=True),
        sg.Text('  DPI '),sg.InputText(fo['@size_dpi'],k='@size_dpi',size=(6,1),enable_events=True),],
        [sg.Checkbox('Tight figure (auto resizing)',k='@tight',default=fo['@tight'],enable_events=True,
        tooltip=' check it on if title is out of the frame. ')],
    ])],
    [sg.Frame(' Color ',layout=[
    [sg.Radio('Black all',"color",k='@c_black',default=fo['@c_black'],pad=(5,0),enable_events=True),
     sg.Radio('Colorful',"color",k='@c_color',default=fo['@c_color'],pad=(5,0),enable_events=True)],
    [sg.Text(' The Color order can be changed in Setting Tab.')],
    ])],
    [sg.Text('Option set:',pad=(0,0)),
    sg.Combo(['DEFAULT']+FIGURE_OPTIONS.sections(),k='@opt_load_name',size=(20,1),default_value=ini_figopt),
    sg.Button('load',k='@b_load_options',pad=(2,0)),
    sg.Button('save',k='@b_save_options',pad=(2,0)),
    sg.Button('del',k='@delete_option_set',button_color=white_bcolor),],
    ])


set_col = sg.Tab(' Setting ',k='TAB_set',layout=[
    [sg.Frame(' Quick starter ',layout=[
    [sg.Text('Initial folder:')],
    [sg.InputText(ini_fo,size=(I_yoko+8,2),k='@s_folder'),
    sg.FolderBrowse(initial_folder=ini_fo,pad=((0,3),3))],
    [sg.Text('Initial Figure Option: '),
    sg.Combo(['DEFAULT']+FIGURE_OPTIONS.sections(),k='@ini_figopt',default_value=ini_figopt,size=(20,1))],
    [sg.Checkbox('Light mode ON',k='@s_light',default=Light)],
    ])],
    [sg.Frame(' Color set ',layout=[
    [sg.Multiline(COLOR_TEXT,k='@c_edit',size=(37,3)),
    sg.Button('reset',k='@b_col_reset',button_color=white_bcolor)],
    [sg.Text('Available color? See: '),
    sg.Text('https://matplotlib.org',k='@link',
    text_color='blue',enable_events=True,size=(20,1),
    tooltip=' https://matplotlib.org/3.3.3/gallery/color/named_colors.html ')],
    ])],
    [sg.Frame(' Window setting ',layout=[[sg.Text('File list row length:',size=(20,1)),
    sg.InputText(file_row,size=(5,1),k='@s_filerow'),sg.Text('default: 8')],
    [sg.Text('Data list row length:',size=(20,1)),
    sg.InputText(data_row,size=(5,1),k='@s_datarow'),sg.Text('default: 5')],
    [sg.Text('Window theme:'),sg.Combo(sg.theme_list(),default_value=THEME,size=(20,1),k='@s_theme')],
    [sg.Checkbox('Disable blurry effect (for Windows)',k='@s_appDPI',default=DPI_mode)],
    ])],
    [sg.Text('')],
    [sg.Button('save settings')],
    ])

How_col = sg.Tab(' How to ',k='TAB_how',layout=[
    [sg.Text('\n1. Select a file (and a folder). \n\n\
2. Add data file(s) to the list. \n\n\
3. A graph is displayed.\n In Light mode, press "refresh" button to show the graph.\n\n\
4. Set options under the list or in the Option tab. \n\n\
5. The figure can be saved as a PNG file. \n\n\
  Before moving to the other dat/DTA Tab,\n\
  Clear the data list.\n\n\
6. If you save the figure option setting, \n  you can use it next time quickly.')]
    ])

Info_col = sg.Tab(' Info ',k='TAB_info',layout=[
    [sg.Text(APP_TITLE,font=('default 16 bold'))],
    [sg.Text('Copyright © AsadaMizue 2021 All rights reserved.')],
    [sg.Text('This is an open-source program.\n\
The source files for the latest version are available from: ')],
    [sg.Text('https://github.com/asada-m/ESR_quick_graphing',
    text_color='blue',enable_events=True,k='@link2')],
    ])

migi_col = sg.Frame('',relief='flat',pad=(0,0),vertical_alignment='top',layout=[
    [sg.Button('refresh'),sg.Button('save figure'),
    sg.Checkbox('Light mode  ',k='@light',default=Light,
    tooltip=' In Light mode, Press "show" to show graph. '),
    ],
    [sg.Image(data=nograph,k='@imgraph')],
    ])

marg_size = (12,1) if DPI_mode else (10,1)
marg_pad = ((15,3),(8,0)) if DPI_mode else (5,(8,0))

LAYOUT = [[sg.Frame('',relief='flat',pad=(0,(0,5)),vertical_alignment='top',layout=[
    [sg.TabGroup([[DTA_col],[DAT_col],[Opt_col],[set_col],[How_col],[Info_col]],pad=(0,0))],
    [sg.Frame('',relief='flat',pad=(0,0),layout=[
    [sg.Text('Separate (%)',size=marg_size,pad=(3,(8,0))),
    sg.Slider(k='@stk',pad=(0,0),range=(0,120),size=(24,10),default_value=0,orientation='h',enable_events=True),
    sg.Button('reset',k='@b_mar_reset',button_color=white_bcolor,pad=marg_pad)],
    [sg.Text('X margin Left',size=marg_size,pad=(3,(8,0))),
    sg.Slider(k='@mar_XL',pad=((0,1),0),range=(5,-49),size=(12,10),default_value=5,orientation='h',enable_events=True),
    sg.Slider(k='@mar_XR',pad=((1,0),0),range=(-49,5),size=(12,10),default_value=5,orientation='h',enable_events=True),
    sg.Text('Right',pad=marg_pad)],
    [sg.Text('Y margin Low',size=marg_size,pad=(3,(8,0))),
    sg.Slider(k='@mar_YL',pad=((0,1),0),range=(10,-49),size=(12,10),default_value=5,orientation='h',enable_events=True),
    sg.Slider(k='@mar_YH',pad=((1,0),0),range=(-49,10),size=(12,10),default_value=5,orientation='h',enable_events=True),
    sg.Text('High',pad=marg_pad)],
#    [sg.Text('Y margin',size=marg_size,pad=(3,(8,0))),
#    sg.Slider(k='@mar_Ya',pad=(0,0),range=(10,-40),size=(24,10),default_value=5,orientation='h',enable_events=True)],
    ])]]),
    migi_col]]

