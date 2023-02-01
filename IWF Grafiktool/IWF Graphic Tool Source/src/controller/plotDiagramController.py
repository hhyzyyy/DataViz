from misc.constants import *
import numpy as np
from matplotlib.lines import Line2D

from model.IWFAxesElement import IWFAxesElement
from model.IWFDiagramElement import IWFDiagramElement
from model.IWFPlotElement import IWFPlotElement

class PlotDiagramController:
    def __init__(self, application):
        self.application = application
        self.mainUi = application.mainUi
        self.legendController = application.legendController

        self.mainPlotElements = [
            IWFPlotElement(self.mainUi.marker1, self.mainUi.colorPicker1, self.mainUi.lineStyle1, self.mainUi.lineStylecolorPicker1),
            IWFPlotElement(self.mainUi.marker2, self.mainUi.colorPicker2, self.mainUi.lineStyle2, self.mainUi.lineStylecolorPicker2),
            IWFPlotElement(self.mainUi.marker3, self.mainUi.colorPicker3, self.mainUi.lineStyle3, self.mainUi.lineStylecolorPicker3),
            IWFPlotElement(self.mainUi.marker4, self.mainUi.colorPicker4, self.mainUi.lineStyle4, self.mainUi.lineStylecolorPicker4),
            IWFPlotElement(self.mainUi.marker5, self.mainUi.colorPicker5, self.mainUi.lineStyle5, self.mainUi.lineStylecolorPicker5)
            ]

        self.secondPlotElements = [
            IWFPlotElement(self.mainUi.marker12, self.mainUi.colorPicker21, self.mainUi.lineStyle21, self.mainUi.lineStylecolorPicker21),
            IWFPlotElement(self.mainUi.marker22, self.mainUi.colorPicker22, self.mainUi.lineStyle22, self.mainUi.lineStylecolorPicker22),
            IWFPlotElement(self.mainUi.marker32, self.mainUi.colorPicker23, self.mainUi.lineStyle23, self.mainUi.lineStylecolorPicker23),
            IWFPlotElement(self.mainUi.marker42, self.mainUi.colorPicker24, self.mainUi.lineStyle24, self.mainUi.lineStylecolorPicker24),
            IWFPlotElement(self.mainUi.marker52, self.mainUi.colorPicker25, self.mainUi.lineStyle25, self.mainUi.lineStylecolorPicker25)
            ]

        self.plotElements = []
        self.plotElements.extend(self.mainPlotElements)
        self.plotElements.extend(self.secondPlotElements)

        self.errorElement = IWFPlotElement(None, self.mainUi.colorPickerError, None, None)

        self.diagramElementMain = IWFDiagramElement(
            self.mainUi.diagramType,
            self.mainUi.markerSize,
            self.mainUi.barWidth,
            self.mainUi.rimWidth,
            self.mainUi.lineWidth,
            self.mainUi.barOffset
        )

        self.diagramElementSecondary = IWFDiagramElement(
            self.mainUi.diagramType2,
            self.mainUi.markerSize2,
            self.mainUi.barWidth2,
            self.mainUi.rimWidth2,
            self.mainUi.lineWidth2,
            self.mainUi.barOffset2
        )

        self.symbolMap = {}

        for index, (key, val) in enumerate(Line2D.markers.items()):
            self.symbolMap[index] = key
            for i, element in enumerate(self.mainPlotElements):
                element.symbol.addItem(val)
                element.symbol.setCurrentText(DEFAULT_SYMBOLS[i])
            for i, element in enumerate(self.secondPlotElements):
                element.symbol.addItem(val)
                element.symbol.setCurrentText(DEFAULT_SYMBOLS[i])

    def handle_plot(self):
        xAxis = self.application.axesController.xAxis
        yAxis = self.application.axesController.yAxis
        axEl = IWFAxesElement(xAxis, yAxis, self.diagramElementMain, self.mainPlotElements, True, self.mainUi.errorAxes.currentIndex() in [ERROR_AXES_MAIN, ERROR_AXES_BOTH])

        self.plot_on_axe(axEl)

        if self.application.dataHandler.has_second_axes():
            xAxis2 = self.application.axesController.xAxis2
            yAxis2 = self.application.axesController.yAxis2
            axEl2 = IWFAxesElement(xAxis2, yAxis2, self.diagramElementSecondary, self.secondPlotElements, False, self.mainUi.errorAxes.currentIndex() in [ERROR_AXES_SECOND, ERROR_AXES_BOTH])

            self.plot_on_axe(axEl2)

    def plot_on_axe(self, axesElement):
        colors = axesElement.get_colors()
        colorsLine = axesElement.get_colors_lines()
        markers = axesElement.get_markers(self.symbolMap)
        lineStyle = axesElement.get_line_style()
        legends = axesElement.get_legend(self.legendController)

        for i in range(min(PLOT_ELEMENT_SIZE, len(axesElement.Y))):
            if axesElement.diagramElement.diagramType.currentText() == SCATTER_WITH_LINE:
                self.create_scatter_plot(axesElement, colors, markers, legends, i)
                self.create_line_plot(axesElement, colorsLine, ['']*len(axesElement.plotElements), lineStyle, i)
            elif axesElement.diagramElement.diagramType.currentText() == SCATTER_NO_LINE:
                self.create_scatter_plot(axesElement, colors, markers, legends, i)
            elif axesElement.diagramElement.diagramType.currentText() == LINE_DIAGRAM:
                self.create_line_plot(axesElement, colorsLine, legends, lineStyle, i)
            else:
                self.create_bar_plot(axesElement, colors, legends, i)

            if axesElement.showError:
                self.create_error_indicator(axesElement, i)

    def get_bar_plot_xpos_and_width(self, axesElement, i):
        w = 1/min(axesElement.Y.shape[0] + 1, PLOT_ELEMENT_SIZE + 1)
        xt = self.get_bar_plot_ticks(axesElement.get_x())
        xpos = xt+w*i+w/2
        barWidthPercent = axesElement.diagramElement.barWidth.value()
        n_width = w*barWidthPercent

        return xpos+n_width*(1-barWidthPercent), n_width

    def calculate_error(self, x, Y, i):
        yerr = self.calculate_error_y(Y, i)
        xerr = self.calculate_error_x(x)
        
        return yerr, xerr

    def calculate_error_x(self, x):
        if not self.mainUi.activateError.isChecked():
            return 0
        xerr = 0

        if self.mainUi.errorType2.currentIndex() == ERROR_TYPE_CONSTANT_INDEX:
            xerr = self.mainUi.errorValue2.value()
        elif self.mainUi.errorType2.currentIndex() == ERROR_TYPE_PERCENT_INDEX:
            xerr = x*self.mainUi.errorValue2.value()/100
        elif self.mainUi.errorType2.currentIndex() == ERROR_TYPE_DEVIATION_INDEX:
            xerr = np.std(x)
        elif self.mainUi.errorType2.currentIndex() == ERROR_TYPE_STANDARD_INDEX:
            xerr = np.std(x, ddof=int(self.mainUi.errorValue2.value())) / np.sqrt(np.size(x))
        elif self.mainUi.errorType2.currentIndex() == ERROR_TYPE_USER_INDEX:
            xerr = self.application.dataHandler.get_df_column_for_error(self.mainUi.errorIndicatorColumn2.currentText())
        return xerr

    def calculate_error_y(self, Y, i):
        if not self.mainUi.activateError.isChecked():
            return 0
        yerr = 0
        if self.mainUi.errorType.currentIndex() == ERROR_TYPE_CONSTANT_INDEX:
            yerr = self.mainUi.errorValue.value()
        elif self.mainUi.errorType.currentIndex() == ERROR_TYPE_PERCENT_INDEX:
            yerr = Y.iloc[i]*self.mainUi.errorValue.value()/100
        elif self.mainUi.errorType.currentIndex() == ERROR_TYPE_DEVIATION_INDEX:
            yerr = np.std(Y.iloc[i])
        elif self.mainUi.errorType.currentIndex() == ERROR_TYPE_STANDARD_INDEX:
            yerr = np.std(Y.iloc[i], ddof=int(self.mainUi.errorValue.value())) / np.sqrt(np.size(Y.iloc[i]))
        elif self.mainUi.errorType.currentIndex() == ERROR_TYPE_USER_INDEX:
            yerr = self.application.dataHandler.get_df_column_for_error(self.mainUi.errorIndicatorColumn.currentText())
        return yerr


    def create_error_indicator(self, axesElement, i):
        if self.mainUi.diagramType.currentText() in BAR_DIAGRAM or not self.mainUi.activateError.isChecked():
            return

        if self.mainUi.diagramType.currentText() == LINE_DIAGRAM and self.mainUi.activateError.isChecked():
                self.application.actionHandler.display_status_info(INFO_ERRORS_ON_LINES)

        yerr, xerr = self.calculate_error(axesElement.get_x(), axesElement.Y, i)

        e_bar = axesElement.axes.errorbar(
            axesElement.get_x(), 
            axesElement.Y.iloc[i], 
            xerr = xerr, 
            yerr = yerr, 
            capsize=self.mainUi.errorCapSize.value(),
            linestyle='none', 
            ecolor=self.errorElement.to_rgb_reference(), 
            zorder = 150)
        for b in e_bar[1]:
            b.set_clip_on(False)
    
    def create_scatter_plot(self, axesElement, colors, markers, legends, i):
        axesElement.axes.scatter(
            axesElement.get_x(), 
            axesElement.Y.iloc[i], 
            color=colors[i], 
            marker = markers[i], 
            clip_on = False, 
            zorder = 200, 
            label = legends[i],
            edgecolors= COLOR_BLACK, 
            linewidth=axesElement.diagramElement.rimWidth.value(), 
            s = axesElement.diagramElement.markerSize.value()**2
            )

    def create_line_plot(self, axesElement, colors, legends, linestyle, i):
        axesElement.axes.plot(
            axesElement.get_x(), 
            axesElement.Y.iloc[i], 
            color=colors[i], 
            label = legends[i], 
            linestyle = linestyle[i],
            linewidth = axesElement.diagramElement.lineWidth.value(), 
            zorder = 1
            )

    def create_bar_plot(self, axesElement, colors, legends, i):
        
        xpos, n_width = self.get_bar_plot_xpos_and_width(axesElement, i)

        yerr = self.calculate_error_y(axesElement.Y, i) if axesElement.showError and axesElement.showError else None
        
        axesElement.axes.bar(
            xpos + axesElement.diagramElement.barOffset.value(), 
            axesElement.Y.iloc[i], 
            width=n_width, 
            yerr = yerr, 
            ecolor=self.errorElement.to_rgb_reference(), 
            capsize = 0 if not self.mainUi.activateError.isChecked() else self.mainUi.errorCapSize.value(),
            color=colors[i], 
            label = legends[i], 
            align='edge', 
            linewidth = axesElement.diagramElement.rimWidth.value(), 
            zorder = 100, 
            edgecolor = COLOR_BLACK)
    
    def get_bar_plot_ticks(self, x):
        return np.arange(x.shape[0])