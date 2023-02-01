from misc.constants import *
import misc.transform as trf

class IWFAxesElement:
    def __init__(self, xAxis, yAxis, diagramElement, plotElements, isMain, showError):
        self.x = xAxis.data
        self.Y = yAxis.data
        self.xAxis = xAxis
        self.yAxis = yAxis
        self.axes = xAxis.axes #or yAxis.axes
        self.diagramElement = diagramElement
        self.plotElements = plotElements
        self.isMain = isMain
        self.showError = showError

    def get_colors(self):        
        rgbs = []
        for element in self.plotElements:
            rgbs.append(element.to_rgb_reference())

        return rgbs
    
    def get_colors_lines(self):        
        rgbs = []
        for element in self.plotElements:
            rgbs.append(element.to_rgb_reference_line())

        return rgbs

    def get_line_style(self):
        styles = []
        for element in self.plotElements:
            styles.append(element.get_line_styles())

        return styles

    def get_markers(self, symbolMap):
        marker_symbol = []
        for element in self.plotElements:
            marker_symbol.append(symbolMap[element.symbol.currentIndex()])
        return marker_symbol

    def get_legend(self, legendController):
        return legendController.get_legend_texts(self.isMain)

    def get_x(self):
        if self.xAxis.isBarInFigure or not trf.is_float(self.x):
            return self.x.index + 0.5

        return self.x.astype(float)
            
        
