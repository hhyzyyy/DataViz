import sys

from qtpy import QtWidgets, QtGui
from view.mainWindow import Ui_MainWindow

from misc.constants import *

from controller.plotLegendController import PlotLegendController
from controller.plotDiagramController import PlotDiagramController
from controller.plotAxesController import PlotAxesController
from controller.plotDescriptionController import PlotDescriptionController
from controller.plotFigureController import PlotFigureController
from controller.fontController import FontController
from controller.guiController import GuiController

from handler.actionHandler import ActionHandler
from handler.dataHandler import DataHandler
from handler.settingHandler import SettingHandler

from model.CheckableComboBox import CheckableComboBox


class Application(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainUi = Ui_MainWindow()
        self.mainUi.setupUi(self)

        self.setWindowIcon(QtGui.QIcon('.\default_settings\icon.ico'))
        self.setWindowTitle(TOOL_NAME)

        self.y_selected_columns = CheckableComboBox()
        self.y_selected_columns.setObjectName(DROPDOWN_Y_NAME)
        self.y_selected_columns2 = CheckableComboBox()
        self.y_selected_columns2.setObjectName(DROPDOWN_Y2_NAME)

        self.widgets = [self.y_selected_columns, self.y_selected_columns2]
        for allowed_widgets in ALLOWED_WIDGETS:
            for child in self.mainUi.centralwidget.findChildren(allowed_widgets):
                if NOT_ALLOWED_WIDGET_NAME != child.objectName():
                    self.widgets.append(child)

        self.dataHandler = DataHandler(self)
        self.actionHandler = ActionHandler(self)
        self.settingHandler = SettingHandler(self)

        self.legendController = PlotLegendController(self)
        self.diagramController = PlotDiagramController(self)
        self.axesController = PlotAxesController(self)
        self.descriptionController = PlotDescriptionController(self)
        self.figureController = PlotFigureController(self)
        self.fontController = FontController(self)
        self.guiController = GuiController(self)

        self.scene = QtWidgets.QGraphicsScene()
        self.mainUi.graphicsView.setScene(self.scene)

    def replace_placeholder_widgets(self):
        self.y_selected_columns.addItem('')
        self.y_selected_columns2.addItem('')

        self.mainUi.placeHolderLayoutMain.replaceWidget(self.mainUi.yAxisSelected, self.y_selected_columns)
        self.mainUi.placeHolderLayoutSecond.replaceWidget(self.mainUi.yAxisSelected2, self.y_selected_columns2)

    def exit(self):
        app.quit()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = Application()
    window.replace_placeholder_widgets()

    window.actionHandler.connectActions()
    window.settingHandler.open_default_settings()

    window.show()
    sys.exit(app.exec_())
