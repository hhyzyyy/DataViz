from misc.constants import *

import configparser
import codecs

from qtpy import QtWidgets, QtCore
from model.CheckableComboBox import CheckableComboBox

class SettingHandler:
    def __init__(self, application):
        self.application = application

    def load_settings(self, config):
        self.application.actionHandler.toggle_event_connection()

        #we have to do this at first, because the table defines the elements of some dropdown widgets
        self.populate_table(config)

        for widget in self.application.widgets:
            if widget.objectName() in config[SERIALIZABLE_GROUP]:
                config_string = codecs.decode(config[SERIALIZABLE_GROUP][widget.objectName()], 'unicode-escape')
                if config_string.startswith('"') and config_string.endswith('"'):
                    config_string = config_string[1:-1]
                if isinstance(widget, QtWidgets.QPlainTextEdit):
                    widget.setPlainText(config_string)
                elif isinstance(widget, QtWidgets.QLineEdit):
                    widget.setText(config_string)
                elif isinstance(widget, QtWidgets.QDoubleSpinBox):
                    widget.setValue(float(config_string))
                elif isinstance(widget, QtWidgets.QCheckBox):
                    widget.setCheckState(int(config_string))
                elif isinstance(widget, CheckableComboBox):
                    widget.setCurrentIndices(config_string.strip('][').split(', '))
                elif isinstance(widget, QtWidgets.QComboBox):
                    widget.setCurrentIndex(int(config_string))

        self._load_color_settings(config, self.application.diagramController.mainPlotElements)
        self._load_color_settings(config, self.application.diagramController.secondPlotElements)
        self.application.diagramController.errorElement.setRgb(config[SERIALIZABLE_GROUP][self.application.diagramController.errorElement.colorButton.objectName()])

        self.application.actionHandler.toggle_event_connection()
        self.application.actionHandler.update()

    def _load_color_settings(self, config, elements):
        for el in elements:
            if el.colorButton.objectName() in config[SERIALIZABLE_GROUP]:
                el.setRgb(config[SERIALIZABLE_GROUP][el.colorButton.objectName()])
            if el.lineStyleColorBotton.objectName() in config[SERIALIZABLE_GROUP]:
                el.setRgbLine(config[SERIALIZABLE_GROUP][el.lineStyleColorBotton.objectName()])

    def populate_table(self, config):
        tableSettings = self.get_config_string(config, self.application.mainUi.tableWidget)
        self.application.dataHandler.create_from_settings(tableSettings)

    def get_config_string(self, config, widget):
        return codecs.decode(config[SERIALIZABLE_GROUP][widget.objectName()], 'unicode-escape')

    def open_default_settings(self):
        config = configparser.ConfigParser()
        config.read(TOOL_DEFAULT_FILE)

        self.load_settings(config)

    def open_settings(self):
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self.application, 'Open file', '', TOOL_FILE)
        if fname:
            config = configparser.ConfigParser()
            config.read(fname)

            self.load_settings(config)

    def save_settings(self):
        fileName, _  = QtWidgets.QFileDialog.getSaveFileName(self.application, " File dialog ", "", TOOL_FILE, "")

        if fileName:
            settings = QtCore.QSettings(fileName, QtCore.QSettings.IniFormat)
            settings.beginGroup(SERIALIZABLE_GROUP)
            for widget in self.application.widgets:
                if isinstance(widget, QtWidgets.QPlainTextEdit):
                    settings.setValue(widget.objectName(), widget.toPlainText().replace('%','%%'))
                elif isinstance(widget, QtWidgets.QLineEdit):
                    settings.setValue(widget.objectName(), widget.text().replace('%','%%'))
                elif isinstance(widget, QtWidgets.QDoubleSpinBox):
                    settings.setValue(widget.objectName(), widget.value())
                elif isinstance(widget, QtWidgets.QCheckBox):
                    settings.setValue(widget.objectName(), widget.checkState())
                elif isinstance(widget, CheckableComboBox):
                    settings.setValue(widget.objectName(), str(widget.currentIndices()))
                elif isinstance(widget, QtWidgets.QComboBox):
                    settings.setValue(widget.objectName(), widget.currentIndex())
                elif isinstance(widget, QtWidgets.QTableWidget):
                    settings.setValue(widget.objectName(), self.application.dataHandler.df.to_csv())
            
            self._save_color_settings(settings, self.application.diagramController.mainPlotElements)
            self._save_color_settings(settings, self.application.diagramController.secondPlotElements)
            settings.setValue(self.application.diagramController.errorElement.colorButton.objectName(), str(self.application.diagramController.errorElement.getRgb()))

            settings.endGroup()
        self.application.actionHandler.display_status_info(INFO_SAVE_SUCCESS)

    def _save_color_settings(self, settings, elements):
        for el in elements:
                settings.setValue(el.colorButton.objectName(), str(el.getRgb()))
                settings.setValue(el.lineStyleColorBotton.objectName(), str(el.getRgbLine()))
