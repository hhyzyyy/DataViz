import pandas as pd
from misc.constants import *
from qtpy import QtWidgets
import misc.transform as trf
from io import StringIO

class DataHandler:
    def __init__(self, application):
        self.application = application
        self.mainUi = application.mainUi

        self.df = pd.DataFrame()

    def get_x_Y(self):
        x, Y = self._df_to_xy(x_index = self.mainUi.xAxisSelected.currentIndex(), y_column_names = self.application.y_selected_columns.currentData())

        return x, Y
    
    def get_second_x_Y(self):
        has_second_x = self.mainUi.xAxisSelected2.currentIndex() != EMPTY_X_AXIS_INDEX
        has_second_y = self.application.y_selected_columns2.currentIndices()

        x, Y = pd.DataFrame(), pd.DataFrame()

        if has_second_x and self.mainUi.shareY.isChecked():
            x, Y = self._df_to_xy(x_index = self.mainUi.xAxisSelected2.currentIndex()-1, y_column_names = self.application.y_selected_columns.currentData())
        elif not has_second_x and self.mainUi.shareY.isChecked():
            x, Y = self._df_to_xy(x_index = self.mainUi.xAxisSelected.currentIndex(), y_column_names = self.application.y_selected_columns.currentData())
        elif has_second_x and has_second_y:
             # a new x- and y-axis must be added and a new plot is generated
            x, Y = self._df_to_xy(x_index = self.mainUi.xAxisSelected2.currentIndex()-1, y_column_names = self.application.y_selected_columns2.currentData())
        elif has_second_x and not has_second_y: 
            #only two x-axis no need to plot the y data again
            x, Y = self._df_to_xy(x_index = self.mainUi.xAxisSelected2.currentIndex()-1, y_column_names = [])
        elif not has_second_x and has_second_y: 
            # no second x-axis, so the y-data is orientated at the main x-axis
            x, Y = self._df_to_xy(x_index = self.mainUi.xAxisSelected.currentIndex(), y_column_names = self.application.y_selected_columns2.currentData())

        return x, Y

    def has_second_axes(self):
        has_second_x = self.mainUi.xAxisSelected2.currentIndex() != EMPTY_X_AXIS_INDEX
        has_second_y = self.application.y_selected_columns2.currentIndices()

        return has_second_x or has_second_y or self.mainUi.shareY.isChecked()
        
    def _df_to_xy(self, x_index, y_column_names):
        x = self.df.iloc[int(self.mainUi.rowFrom.value()):int(self.mainUi.rowUntil.value())+1, x_index]
        Y = self.df.loc[int(self.mainUi.rowFrom.value()):int(self.mainUi.rowUntil.value()),y_column_names]

        isBarInFigure = self.mainUi.diagramType.currentText() == BAR_DIAGRAM or (self.has_second_axes() and self.mainUi.diagramType2.currentText() == BAR_DIAGRAM)

        # if there is a bar in the plot we have to interpret every x-value as string and otherwise it has to be a float
        if not isBarInFigure and trf.is_float(x):
            x = x.astype(float)

        if not trf.is_float(Y):
            self.application.actionHandler.display_status_error(ERROR_NO_STRINGS_Y)
            raise ValueError

        return x, Y.astype(float).T

    def get_df_column_for_error(self, name):
        if trf.is_float(self.df.loc[int(self.mainUi.rowFrom.value()):int(self.mainUi.rowUntil.value()), name]):
            return self.df.loc[int(self.mainUi.rowFrom.value()):int(self.mainUi.rowUntil.value()), name].astype(float).to_list()
        
        self.application.actionHandler.display_status_error(ERROR_ONLY_NUMBERS)
        raise ValueError

    def create_from_settings(self, data):
        self.df = pd.read_csv(StringIO(data.strip('"')))
        self.df = self.df.iloc[: , 1:].dropna(axis = 1, how = 'all').dropna(axis = 0, how = 'all')

        self.populate_table() 

    def get_row_count(self):
        return self.df.shape[0]

    def create_from_sheet(self, fname):
        self.df = pd.read_excel(fname[0]) if READ_EXCEL_TYPE in fname[1] else pd.read_csv(fname[0])
        self.df = self.df.dropna(axis = 1, how = 'all').dropna(axis = 0, how = 'all')

        self.application.actionHandler.toggle_event_connection()
        self.populate_table()

        self.application.actionHandler.toggle_event_connection()
        self.application.actionHandler.update()

    def populate_table(self):
        self.mainUi.tableWidget.clear()
        self.mainUi.tableWidget.setRowCount(0)

        self.mainUi.tableWidget.setColumnCount(self.df.shape[1])
        self.mainUi.tableWidget.setHorizontalHeaderLabels(self.df.columns)
        self.mainUi.tableWidget.resizeColumnsToContents()

        for pos in range(min(self.df.shape[0], MAX_ROWS)):
            self.mainUi.tableWidget.insertRow(pos)
            for ind in range(self.df.shape[1]):
                item = QtWidgets.QTableWidgetItem(str(self.df.iat[pos,ind]))
                self.mainUi.tableWidget.setItem(pos, ind, item)

        self.populate_referenced_widgets()

    def populate_referenced_widgets(self):
        self.mainUi.xAxisSelected.clear()
        self.mainUi.xAxisSelected2.clear()
        self.mainUi.errorIndicatorColumn.clear()
        self.mainUi.errorIndicatorColumn2.clear()

        self.mainUi.xAxisSelected2.addItem('')

        for col in self.df.columns:
            self.mainUi.xAxisSelected.addItem(col)
            self.mainUi.xAxisSelected.setCurrentIndex(FIRST_INDEX_X_AXIS)

            self.mainUi.xAxisSelected2.addItem(col)
            self.mainUi.xAxisSelected2.setCurrentIndex(EMPTY_X_AXIS_INDEX)

            self.mainUi.errorIndicatorColumn.addItem(col)
            self.mainUi.errorIndicatorColumn.setCurrentIndex(FIRST_INDEX_X_AXIS)

            self.mainUi.errorIndicatorColumn2.addItem(col)
            self.mainUi.errorIndicatorColumn2.setCurrentIndex(FIRST_INDEX_X_AXIS)

        self.application.y_selected_columns.setItems(self.df.columns)
        self.application.y_selected_columns2.setItems(self.df.columns)

        self.application.y_selected_columns.updateText()
        self.application.y_selected_columns2.updateText()

        self.mainUi.rowFrom.setValue(0)
        self.mainUi.rowUntil.setMaximum(self.df.shape[0] - 1)
        self.mainUi.rowUntil.setValue(self.df.shape[0] - 1)