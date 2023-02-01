from qtpy import QtWidgets

TOOL_NAME                   = 'IWF Graphic Tool'

CM                          = 1/2.54 #inch to cm
MAX_RGB_VALUE               = 255
MAX_ROWS                    = 5 #this is the maximal amount of data rows that are shown in the gui
MAX_Y_TICKS                 = 5
MAX_X_TICKS                 = 5 #doesn't come into account for bar plots
UNIT_POSITION               = -2
INVALID_FIGURE_ALPHA        = 127
PLOT_ELEMENT_SIZE           = 5 #the amount of possible plots on axes
MAX_ALLOWED_DATAROWS        = 100 #defines when only line plots are possible
STATUSBAR_MESSAGE_DURATION  = 60*1*1000

ALLOWED_WIDGETS             = [QtWidgets.QPlainTextEdit, QtWidgets.QLineEdit, QtWidgets.QDoubleSpinBox, QtWidgets.QCheckBox, QtWidgets.QComboBox, QtWidgets.QTableWidget]
NOT_ALLOWED_WIDGET_NAME     = 'qt_spinbox_lineedit'
COLOR_BLACK                 = '#000000'
DEFAULT_SYMBOLS             = ['triangle_up', 'square', 'diamond', 'circle', 'plus_filled']
MATHMODE_NO_SPACE           = '$\!$' #when using the mathmode the text is slightly out of line, by adding this to every line we ensure that all texts look the same

### Saving/Loading ###
TOOL_FILE                   = "IWF Graphic File (*.igf)"
TOOL_DEFAULT_FILE           = 'default_settings/default_0.igf'
SERIALIZABLE_GROUP          = "Setting"
DATA_FILES                  = "Excel Dateien (*.xls *.xlsx);;CSV Dateien (*.csv)"
READ_EXCEL_TYPE             = 'Excel Dateien'

### Matplotlib font settings ###
FONT_SIZE                   = 'font.size'
FONT_FAMILY                 = 'font.family'
MATHTEXT_FONTSET            = 'mathtext.fontset'
MATHTEXT_FONTSET_VALUE      = 'custom'
MATHTEXT_DEFAULT            = 'mathtext.default'
MATHTEXT_DEFAULT_VALUE      = 'regular'
MATHTEXT_BF                 = 'mathtext.bf'
MATHTEXT_SF                 = 'mathtext.sf'
MATHTEXT_RM                 = 'mathtext.rm'
MATHTEXT_IT                 = 'mathtext.it'
TIMES_NEW_ROMAN             = "Times New Roman"
TIMES_FAMILY                = 'serif'

### Messages ###
WARNING_TO_MUCH_DATA        = f'Datensätze mit mehr als {MAX_ALLOWED_DATAROWS} Datenreihen werden aus stilistischen Gründen nur als Liniendiagramme angezeigt. Zudem wurden die Fehlerindikatoren deaktiviert.'
INFO_ERRORS_ON_LINES        = 'Fehlerindikatoren bei Liniendiagrammen sind unschön. Nutzen Sie lieber Scatter- oder Balkendiagramme!'
WARNING_LARGE_FILES         = 'Hinweis: Eine CSV Datei kann sehr viel schneller eingelesen werden als eine Excel Datei!'
ERROR_UNREADABLE_FILE       = 'Die Datei kann nicht geladen werden. Bitte überprüfen Sie ob die Datei im richtigen Format ist.'
ERROR_BROKEN_FIGURE         = 'Die Grafik kann mit den aktuellen Einstellungen nicht erstellt werden.'
ERROR_NO_STRINGS_Y          = 'y-Werte dürfen keine Strings sein!'
ERROR_ONLY_NUMBERS          = 'Bitte wählen Sie eine Spalte die nur Zahlen enthält! Strings können kein Fehler sein.'
INFO_SAVE_SUCCESS           = 'erfolgreich gespeichert'
ERROR_PERMISSION_DENIED     = 'Die Datei kann nicht überschrieben werden. Eventuell ist die Datei noch irgendwo anders geöffnet.'

### Messages Style ###
ERROR_MESSAGE_STYLE         = "QStatusBar{background:rgba(255,0,0,255);color:black;font-weight:bold;}"
WARNING_MESSAGE_STYLE       = "QStatusBar{background:rgba(255,255,0,255);color:black;font-weight: bold;}"
INFO_MESSAGE_STYLE          = "QStatusBar{font-weight: bold;}"

### Labels ###
ERROR_TYPE_CONSTANT         = 'Zahlenwert'
ERROR_TYPE_PERCENT          = 'Prozentsatz'
ERROR_TYPE_STANDARD         = 'Freiheitsgrade'
COLOR_TEXT                  = 'background-color: {rgb};'

# !!! Changes in the next few paraphs will break the GUI and changes in the QT ui file are needed as well. !!! #

FIRST_INDEX_X_AXIS          = 0
EMPTY_X_AXIS_INDEX          = 0 
DROPDOWN_Y_NAME             = 'y_selected_columns'
DROPDOWN_Y2_NAME            = 'y_selected_columns2'
LANGUAGE_TO_LOCALE          = {'Englisch' : 'en', 'Deutsch' : 'de'}
DEFAULT_LANGUAGE            = 'Deutsch'

### Diagramtypes ###
BAR_DIAGRAM                 = 'Balkendiagramm'
BAR_DIAGRAM_INDEX           = 0
SCATTER_WITH_LINE           = 'Scatter mit Linien'
SCATTER_WITH_LINE_INDEX     = 1
SCATTER_NO_LINE             = 'Scatter ohne Linien'
SCATTER_NO_LINE_INDEX       = 2
LINE_DIAGRAM                = 'Liniendiagramm'
LINE_DIAGRAM_INDEX          = 3

### Page indices of the toolbox with 'Beschriftung', 'Achsen', 'Legende', 'Fehlerindikatoren' ###
TOOLBOX_DESCRIPTION_INDEX   = 0
TOOLBOX_AXES_INDEX          = 1
TOOLBOX_LEGEND_INDEX        = 2
TOOLBOX_ERROR_INDEX         = 3
TOOLBOX_AXES_X_INDEX        = 0
TOOLBOX_AXES_Y_INDEX        = 1
TOOLBOX_AXES_X2_INDEX       = 2
TOOLBOX_AXES_Y2_INDEX       = 3
TOOLBOX_LEGEND_MAIN_AXES    = 0
TOOLBOX_LEGEND_SECOND_AXES  = 1

### Indices of axes that should show an error ###
ERROR_AXES_MAIN             = 0
ERROR_AXES_SECOND           = 1
ERROR_AXES_BOTH             = 2

### Indices of error type dropdown ###
ERROR_TYPE_CONSTANT_INDEX   = 0
ERROR_TYPE_PERCENT_INDEX    = 1
ERROR_TYPE_DEVIATION_INDEX  = 2
ERROR_TYPE_STANDARD_INDEX   = 3
ERROR_TYPE_USER_INDEX       = 4

### Axes positions ###
X_POSITION_TOP              = 'oben'
X_POSITION_BOTTOM           = 'unten'
Y_POSITION_LEFT             = 'links'
Y_POSITION_RIGHT            = 'rechts'