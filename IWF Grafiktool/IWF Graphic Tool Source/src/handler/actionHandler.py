from qtpy import QtWidgets, QtGui
from misc.constants import *

from functools import partial

class ActionHandler:
    def __init__(self, application):
        self.application = application
        self.mainUi = application.mainUi
        self.statusBar = application.mainUi.statusBar

        self.connect = False
        self.error = False

        self.colorDialog = QtWidgets.QColorDialog()
        self.colorDialog.setCustomColor(0, QtGui.QColor(0, 0, 0, 1))
        self.colorDialog.setCustomColor(2, QtGui.QColor(MAX_RGB_VALUE, MAX_RGB_VALUE, MAX_RGB_VALUE, 1))
        self.colorDialog.setCustomColor(4, QtGui.QColor(159, 182, 196, 1))
        self.colorDialog.setCustomColor(6, QtGui.QColor(125, 102, 102, 1))
        self.colorDialog.setCustomColor(8, QtGui.QColor(153, 0, 0, 1))

    def toggle_event_connection(self):
        for widget in self.application.widgets:
            if isinstance(widget, QtWidgets.QLineEdit) or isinstance(widget, QtWidgets.QPlainTextEdit):
                widget.disconnect() if not self.connect else widget.textChanged.connect(self.update)
            elif isinstance(widget, QtWidgets.QDoubleSpinBox):
                widget.disconnect() if not self.connect else widget.valueChanged.connect(self.update)
            elif isinstance(widget, QtWidgets.QCheckBox):
                widget.disconnect() if not self.connect else widget.stateChanged.connect(self.update)
            elif isinstance(widget, QtWidgets.QComboBox):
                widget.disconnect() if not self.connect else widget.currentTextChanged.connect(self.update)

        self.connect = not self.connect

    def connectActions(self):
        self.mainUi.actionBild_exportieren.triggered.connect(self.save_image)
        self.mainUi.actionExit_Alt_F4.triggered.connect(self.application.exit)

        self.mainUi.actionLoadCSV.clicked.connect(self.show_loading_message)

        self.mainUi.actionLoadCSV.clicked.connect(self.load_data_file)

        self.mainUi.actionSave.triggered.connect(self.application.settingHandler.save_settings)
        self.mainUi.action_ffnen.triggered.connect(self.open_settings)
        self.mainUi.actionNew.triggered.connect(self.application.settingHandler.open_default_settings)

        self._connectColorAction(self.application.diagramController.mainPlotElements)
        self._connectColorAction(self.application.diagramController.secondPlotElements)
        self.application.diagramController.errorElement.colorButton.clicked.connect(partial(self.openColorDialog, self.application.diagramController.errorElement))

    def _connectColorAction(self, elements):
        for el in elements:
            el.colorButton.clicked.connect(partial(self.openColorDialog, el))
            el.lineStyleColorBotton.clicked.connect(partial(self.openColorDialog, el, True))

    def open_settings(self):
        self.application.settingHandler.open_settings()
    
    def show_loading_message(self):
        self.display_status_warning(WARNING_LARGE_FILES)
        self.mainUi.centralwidget.setEnabled(False)

    def load_data_file(self):
        try:
            fname = QtWidgets.QFileDialog.getOpenFileName(self.application, 'Open file', '', DATA_FILES)

            if fname and fname[0] != '':
                self.application.dataHandler.create_from_sheet(fname)
            self.display_status_info('')
        except ValueError:
            self.display_status_error(ERROR_UNREADABLE_FILE)
        self.mainUi.centralwidget.setEnabled(True)

    def openColorDialog(self, iwfPlotElement, isLine = False):
        color = self.colorDialog.getColor()
        if color.isValid():
            if isLine:
                iwfPlotElement.updateLine(color)
            else:
                iwfPlotElement.update(color)
            self.update()

    def save_image(self):
        if self.error:
            self.display_status_error(ERROR_BROKEN_FIGURE)
        else:
            filters = ''
            for key, value in self.application.figureController.figure.canvas.get_supported_filetypes().items():
                filters += f'{value} (*.{key});;'

            fileName, _  = QtWidgets.QFileDialog.getSaveFileName(self.application, " File dialog ", "", filters, "")

            if fileName and self.application.figureController.figure:
                try:
                    self.application.figureController.figure.savefig(fileName, transparent = self.mainUi.transparent.isChecked())
                except PermissionError:
                    self.display_status_error(ERROR_PERMISSION_DENIED)
                except RuntimeError as e:
                    self.display_status_error(str(e))

    def display_status_message(self, message, duration = STATUSBAR_MESSAGE_DURATION):
        self.statusBar.clearMessage()
        self.statusBar.showMessage(message, duration)

    def display_status_info(self, info=''):
        self.statusBar.setStyleSheet(INFO_MESSAGE_STYLE)
        self.display_status_message(info)

    def display_status_warning(self, warning):
        self.statusBar.setStyleSheet(WARNING_MESSAGE_STYLE)
        self.display_status_message(warning)

    def display_status_error(self, error):
        self.statusBar.setStyleSheet(ERROR_MESSAGE_STYLE)
        self.display_status_message(error)

    def update(self):
        try:            
            self.display_status_info()
            self.error = False

            self.application.guiController.handle_gui_element_visibility()
            self.application.fontController.update_font()
            self.application.figureController.validate_user_text_input()

            self.application.figureController.create_figure()
            self.application.axesController.create_axes()
            self.application.diagramController.handle_plot()
            self.application.axesController.handle_axes_labels()
            self.application.legendController.handle_legends()
            self.application.descriptionController.handle_main_labels()
            self.application.figureController.repaint_figure()
        except ValueError as e:
            self.display_status_error(str(e))
            self.error = True
            self.application.figureController.disable()



    