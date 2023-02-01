from misc.constants import *

import locale

def is_float(dataframe):
    try:
        dataframe.astype(float)
        return True
    except ValueError:
        return False

def float_locale_string(number, language = DEFAULT_LANGUAGE, decimals = 2):
    locale.setlocale(locale.LC_ALL, LANGUAGE_TO_LOCALE[language])
    return locale.format(f'%.{decimals}f', float(number), 1)

def list_to_float_locale(number_list, language = DEFAULT_LANGUAGE, decimals = 2):
    transformed_list = []
    for entry in number_list:
        if str(entry).isnumeric() or isinstance(entry, float):
            transformed_list.append(float_locale_string(entry, language, decimals))
        else:
            transformed_list.append(entry)
    return transformed_list

def spine_position(value):
    if value == X_POSITION_BOTTOM:
        return 'bottom'
    elif value == X_POSITION_TOP:
        return 'top'
    elif value == Y_POSITION_LEFT:
        return 'left'
    return 'right'

def get_linespace_factor(value):
    factor = 151

    if round(value, 1) == 0.5:
        factor = 87
    elif round(value, 1) == 0.6:
        factor = 95
    elif round(value, 1) == 0.7:
        factor = 101
    elif round(value, 1) == 0.8:
        factor = 110
    elif round(value, 1) == 0.9:
        factor = 115
    elif round(value, 1) == 1.0:
        factor = 117
    elif round(value, 1) == 1.1:
        factor = 120
    elif round(value, 1) == 1.2:
        factor = 123
    elif round(value, 1) == 1.3:
        factor = 126
    elif round(value, 1) == 1.4:
        factor = 130
    elif round(value, 1) == 1.5:
        factor = 133
    elif round(value, 1) in [1.6, 1.7]:
        factor = 135
    elif round(value, 1) in [1.8]:
        factor = 137
    elif round(value, 1) in [1.9, 2.0]:
        factor = 140
    elif round(value, 1) == 2.1:
        factor = 143
    elif round(value, 1) in [2.2, 2.3, 2.4]:
        factor = 145
    elif round(value, 1) == 2.5:
        factor = 147
    elif round(value, 1) in [2.7, 2.8, 2.9]:
        factor = 150

    return factor