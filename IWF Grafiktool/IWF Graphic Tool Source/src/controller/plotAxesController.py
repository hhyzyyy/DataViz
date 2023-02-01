from misc.constants import *
import misc.transform as trf

from mpl_toolkits.axes_grid1 import Divider, Size

from model.IWFAxisElement import IWFAxisElement

class PlotAxesController:
    def __init__(self, application):
        self.application = application
        self.mainUi = application.mainUi

        self.axes = None
        self.twinAxes = None

        self.xAxis = IWFAxisElement(self.axes)
        self.yAxis = IWFAxisElement(self.axes)
        self.xAxis2 = IWFAxisElement(self.twinAxes)
        self.yAxis2 = IWFAxisElement(self.twinAxes)

    def create_axes(self):
        height = self.mainUi.imageHeight.value()

        widthPlot = self.mainUi.width.value()
        heightPlot = self.mainUi.height.value()

        paddingTop = self.mainUi.paddingTop.value()
        paddingLeft = self.mainUi.paddingLeft.value()

        h = [Size.Fixed(paddingLeft*CM), Size.Fixed(widthPlot*CM)]
        v = [Size.Fixed((height - heightPlot-paddingTop)*CM), Size.Fixed(heightPlot*CM)]

        divider = Divider(self.application.figureController.figure, (0, 0, 1, 1), h, v, aspect=False)

        self.axes = self.application.figureController.figure.add_axes(divider.get_position(), axes_locator=divider.new_locator(nx=1, ny=1))
        if self.application.dataHandler.has_second_axes():
            self.twinAxes = self.application.figureController.figure.add_axes(divider.get_position(), axes_locator=divider.new_locator(nx=1, ny=1))

            # since we're painting the two axes at the same position we have to make the top one opaque
            self.twinAxes.patch.set_alpha(0)
            self.twinAxes.spines['left'].set_visible(False)
            self.twinAxes.spines['top'].set_visible(False)
            self.twinAxes.spines['right'].set_visible(False)
            self.twinAxes.spines['bottom'].set_visible(False)

        self.create_axis()

    def create_axis(self):
        x, Y = self.application.dataHandler.get_x_Y()
        x2, Y2 = self.application.dataHandler.get_second_x_Y()

        isBarInFigure = self.application.mainUi.diagramType.currentText() == BAR_DIAGRAM or (Y2.shape[0] > 0 and self.application.mainUi.diagramType2.currentText() == BAR_DIAGRAM)

        self.xAxis = IWFAxisElement(
                    self.axes,
                    x, #data
                    self.mainUi.xLabel.toPlainText(),
                    self.mainUi.xLabelPosition.currentText(),
                    self.mainUi.xUnit.text(),
                    self.mainUi.labelPadX.value(),
                    self.mainUi.xDecimals.value(),
                    self.mainUi.xRotation.value(),
                    isBarInFigure = isBarInFigure,
                    is_active = self.mainUi.activateAxes.isChecked())
        self.yAxis = IWFAxisElement(
                    self.axes,
                    Y, #data
                    self.mainUi.yLabel.toPlainText(),
                    self.mainUi.yLabelPosition.currentText(),
                    self.mainUi.yUnit.text(),
                    self.mainUi.labelPadY.value(),
                    self.mainUi.yDecimals.value(),
                    self.mainUi.yRotation.value(),
                    isX = False,
                    isBarInFigure = isBarInFigure,
                    is_active = self.mainUi.activateAxes.isChecked())
        
        if self.application.dataHandler.has_second_axes():
            self.xAxis2 = IWFAxisElement(
                        self.twinAxes,
                        x2, #data
                        self.mainUi.xLabel2.toPlainText(),
                        self.mainUi.xLabelPosition2.currentText() if self.mainUi.xAxisSelected2.currentIndex() != EMPTY_X_AXIS_INDEX else self.mainUi.xLabelPosition.currentText(),
                        self.mainUi.xUnit2.text(),
                        self.mainUi.labelPadX2.value(),
                        self.mainUi.xDecimals2.value(),
                        self.mainUi.xRotation2.value(),
                        self.mainUi.xOutward.value(),
                        isMain = False,
                        isBarInFigure = isBarInFigure,
                        is_active = self.mainUi.xAxisSelected2.currentIndex() != EMPTY_X_AXIS_INDEX and self.mainUi.activateAxes.isChecked(),
                        parent_position=self.mainUi.xLabelPosition.currentText())
            self.yAxis2 = IWFAxisElement(
                        self.twinAxes,
                        Y2, #data
                        self.mainUi.yLabel2.toPlainText(),
                        self.mainUi.yLabelPosition2.currentText() if not self.mainUi.shareY.isChecked() and self.application.y_selected_columns2.currentIndices() else self.mainUi.yLabelPosition.currentText(),
                        self.mainUi.yUnit2.text(),
                        self.mainUi.labelPadY2.value(),
                        self.mainUi.yDecimals2.value(),
                        self.mainUi.yRotation2.value(),
                        self.mainUi.yOutward.value(),
                        isMain = False,
                        isX = False,
                        isBarInFigure = isBarInFigure,
                        is_active = self.application.y_selected_columns2.currentIndices() and self.mainUi.activateAxes.isChecked() and not self.mainUi.shareY.isChecked(),
                        parent_position=self.mainUi.yLabelPosition.currentText())

    def handle_axes_labels(self):        
        axis_list = [self.xAxis, self.yAxis]
        if self.application.dataHandler.has_second_axes():
            axis_list.extend([self.xAxis2, self.yAxis2])

        if self.mainUi.gridVisible.isChecked():
            self.axes.grid(which='major', color=COLOR_BLACK, linestyle='-', linewidth=self.mainUi.gridWidth.value())

        positions = list(map(lambda axis:axis.label_position, axis_list))

        for axis in axis_list:
            axis.calculate_ticks(baseAxe = self.axes, twinAxe = self.twinAxes, mainUi = self.mainUi, shareY = self.mainUi.shareY.isChecked())
            axis.handle_padding()
            axis.handle_ticks()
            axis.handle_position()
            axis.handle_outward(positions, self.mainUi.axesWidth.value())
            axis.handle_rotation()
            axis.handle_global_activation(self.mainUi.numberFormat.currentText(), self.mainUi.lineSpacing.value())
            axis.handle_tick_activation()

        self.handle_spines(positions)
    
    def handle_spines(self, positions):
        self.axes.spines['left'].set_linewidth(self.mainUi.gridWidth.value())
        self.axes.spines['top'].set_linewidth(self.mainUi.gridWidth.value())
        self.axes.spines['right'].set_linewidth(self.mainUi.gridWidth.value())
        self.axes.spines['bottom'].set_linewidth(self.mainUi.gridWidth.value())

        for pos in positions:
            self.axes.spines[trf.spine_position(pos)].set_linewidth(self.mainUi.axesWidth.value())