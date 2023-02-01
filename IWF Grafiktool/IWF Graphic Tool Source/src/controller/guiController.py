from misc.constants import *

class GuiController:
    def __init__(self, application):
        self.application = application
        self.mainUi = application.mainUi

    def handle_gui_element_visibility(self):
        self.mainUi.rowFrom.setMaximum(self.mainUi.rowUntil.value() - 1)

        self.mainUi.yAxisSelected.hide()
        self.mainUi.yAxisSelected2.hide()

        self.handle_selected_diagram_type(self.application.diagramController.diagramElementMain, self.application.diagramController.mainPlotElements)
        self.handle_selected_diagram_type(self.application.diagramController.diagramElementSecondary, self.application.diagramController.secondPlotElements)
        self.handle_error_indicator()
        self.handle_multiple_axes()
        self.handle_excessive_data()

    def handle_selected_diagram_type(self, diagramElement, plotElements):
        if diagramElement.diagramType.currentText() == LINE_DIAGRAM:
            diagramElement.markerSize.setDisabled(True)
            diagramElement.barWidth.setDisabled(True)
            diagramElement.rimWidth.setDisabled(True)
            diagramElement.lineWidth.setDisabled(False)
            diagramElement.barOffset.setDisabled(True)
        elif diagramElement.diagramType.currentText() == SCATTER_NO_LINE:
            diagramElement.markerSize.setDisabled(False)
            diagramElement.barWidth.setDisabled(True)
            diagramElement.rimWidth.setDisabled(False)
            diagramElement.lineWidth.setDisabled(True)
            diagramElement.barOffset.setDisabled(True)
        elif diagramElement.diagramType.currentText() == SCATTER_WITH_LINE:
            diagramElement.markerSize.setDisabled(False)
            diagramElement.barWidth.setDisabled(True)
            diagramElement.rimWidth.setDisabled(False)
            diagramElement.lineWidth.setDisabled(False)
            diagramElement.barOffset.setDisabled(True)
        elif diagramElement.diagramType.currentText() == BAR_DIAGRAM:
            diagramElement.markerSize.setDisabled(True)
            diagramElement.barWidth.setDisabled(False)
            diagramElement.rimWidth.setDisabled(False)
            diagramElement.lineWidth.setDisabled(True)
            diagramElement.barOffset.setDisabled(False)

        for element in plotElements:
            if diagramElement.diagramType.currentText() == LINE_DIAGRAM:
                element.symbol.hide()
                element.colorButton.hide()
                element.lineStyle.show()
                element.lineStyleColorBotton.show()
            elif diagramElement.diagramType.currentText() == SCATTER_NO_LINE:
                element.symbol.show()
                element.colorButton.show()
                element.lineStyle.hide()
                element.lineStyleColorBotton.hide()
            elif diagramElement.diagramType.currentText() == SCATTER_WITH_LINE:
                element.symbol.show()
                element.colorButton.show()
                element.lineStyle.show()
                element.lineStyleColorBotton.show()
            elif diagramElement.diagramType.currentText() == BAR_DIAGRAM:
                element.symbol.hide()
                element.colorButton.show()
                element.lineStyle.hide()
                element.lineStyleColorBotton.hide()

    def handle_excessive_data(self):
        if self.application.dataHandler.get_row_count() >= MAX_ALLOWED_DATAROWS:
            self.mainUi.diagramType.setCurrentIndex(LINE_DIAGRAM_INDEX)
            self.mainUi.diagramType.setDisabled(True)
            self.mainUi.diagramType2.setCurrentIndex(LINE_DIAGRAM_INDEX)
            self.mainUi.diagramType2.setDisabled(True)
            self.mainUi.toolBox.setItemEnabled(TOOLBOX_ERROR_INDEX, False)

            self.application.actionHandler.display_status_warning(WARNING_TO_MUCH_DATA)
        else:
            self.mainUi.diagramType.setDisabled(False)
            self.mainUi.diagramType2.setDisabled(False)
            self.mainUi.toolBox.setItemEnabled(TOOLBOX_ERROR_INDEX, True)

    def handle_multiple_axes(self):
        if self.mainUi.xAxisSelected2.currentIndex() != EMPTY_X_AXIS_INDEX:
            self.mainUi.toolBoxAxes.setItemEnabled(TOOLBOX_AXES_X2_INDEX, True)
        else:
            self.mainUi.toolBoxAxes.setItemEnabled(TOOLBOX_AXES_X2_INDEX, False)

        if self.application.y_selected_columns2.currentIndices() or self.mainUi.shareY.isChecked():
            self.mainUi.toolBoxAxes.setItemEnabled(TOOLBOX_AXES_Y2_INDEX, True)
        else:
            self.mainUi.toolBoxAxes.setItemEnabled(TOOLBOX_AXES_Y2_INDEX, False)

        if self.application.dataHandler.has_second_axes():
            self.mainUi.toolBoxLegendText.setItemEnabled(TOOLBOX_LEGEND_SECOND_AXES, True)
        else:
            self.mainUi.toolBoxLegendText.setItemEnabled(TOOLBOX_LEGEND_SECOND_AXES, False)

        if self.mainUi.shareY.isChecked():
            self.application.y_selected_columns2.setDisabled(True)
        else:
            self.application.y_selected_columns2.setDisabled(False)

    def _handle_error_indicator(self, type, tLabel, value, col, eLabel):
        if type.currentIndex() == ERROR_TYPE_CONSTANT_INDEX:
            tLabel.setText(ERROR_TYPE_CONSTANT)
            value.setMinimum(0)
            value.setDecimals(2)
            value.setSingleStep(0.01)
            tLabel.show()
            value.show()
            col.hide()
            eLabel.hide()
        elif type.currentIndex() == ERROR_TYPE_PERCENT_INDEX:
            tLabel.setText(ERROR_TYPE_PERCENT)
            value.setMinimum(0)
            value.setDecimals(2)
            value.setSingleStep(0.01)
            tLabel.show()
            value.show()
            col.hide()
            eLabel.hide()
        elif type.currentIndex() == ERROR_TYPE_DEVIATION_INDEX:
            tLabel.hide()
            value.hide()
            col.hide()
            eLabel.hide()
        elif type.currentIndex() == ERROR_TYPE_STANDARD_INDEX:
            tLabel.setText(ERROR_TYPE_STANDARD)
            value.setMinimum(1)
            value.setDecimals(0)
            value.setSingleStep(1)
            tLabel.show()
            value.show()
            col.hide()
            eLabel.hide()
        elif type.currentIndex() == ERROR_TYPE_USER_INDEX:
            tLabel.hide()
            value.hide()
            col.show()
            eLabel.show()

    def handle_error_indicator(self):
        self._handle_error_indicator(self.mainUi.errorType, self.mainUi.errorTypeLabel, self.mainUi.errorValue, self.mainUi.errorIndicatorColumn, self.mainUi.customErrorLabel)
        self._handle_error_indicator(self.mainUi.errorType2, self.mainUi.errorTypeLabel2, self.mainUi.errorValue2, self.mainUi.errorIndicatorColumn2, self.mainUi.customErrorLabel2)
            