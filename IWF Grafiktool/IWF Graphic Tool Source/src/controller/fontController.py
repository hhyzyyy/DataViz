from matplotlib import rcParams
from misc.constants import *

class FontController:
    def __init__(self, application):
        self.application = application
        self.mainUi = application.mainUi

    
    def update_font(self):
        rcParams[FONT_SIZE] = self.mainUi.fontSize.value()
        rcParams[FONT_FAMILY] = TIMES_FAMILY if self.mainUi.font.currentText() == TIMES_NEW_ROMAN else self.mainUi.font.currentText()

        rcParams[MATHTEXT_FONTSET] = MATHTEXT_FONTSET_VALUE
        rcParams[MATHTEXT_DEFAULT] = MATHTEXT_DEFAULT_VALUE

        rcParams[MATHTEXT_BF] = f'{TIMES_FAMILY if rcParams[FONT_FAMILY][0] == TIMES_NEW_ROMAN else rcParams[FONT_FAMILY][0]}:bold'
        rcParams[MATHTEXT_SF] = f'{TIMES_FAMILY if rcParams[FONT_FAMILY][0] == TIMES_NEW_ROMAN else rcParams[FONT_FAMILY][0]}'
        rcParams[MATHTEXT_RM] = f'{TIMES_FAMILY if rcParams[FONT_FAMILY][0] == TIMES_NEW_ROMAN else rcParams[FONT_FAMILY][0]}'
        rcParams[MATHTEXT_IT] = f'{TIMES_FAMILY if rcParams[FONT_FAMILY][0] == TIMES_NEW_ROMAN else rcParams[FONT_FAMILY][0]}:italic'    