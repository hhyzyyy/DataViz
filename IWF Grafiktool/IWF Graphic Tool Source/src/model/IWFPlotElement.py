from misc.constants import *
import misc.constants as CONSTANTS
from qtpy import QtGui

class IWFPlotElement:
    def __init__(self, symbol, colorButton, lineStyle, lineStyleColorBotton):
        self.symbol = symbol
        self.colorButton = colorButton
        self.lineStyle = lineStyle
        self.lineStyleColorBotton = lineStyleColorBotton

        self.color = QtGui.QColor()
        self.colorLine = QtGui.QColor()

    def to_rgb_reference(self):
        return (self.color.red() / MAX_RGB_VALUE, self.color.green() / MAX_RGB_VALUE, self.color.blue() / MAX_RGB_VALUE)

    def to_rgb_reference_line(self):
        return (self.colorLine.red() / MAX_RGB_VALUE, self.colorLine.green() / MAX_RGB_VALUE, self.colorLine.blue() / MAX_RGB_VALUE)

    def get_line_styles(self):
        return self.lineStyle.currentText()

    def getRgb(self):
        return self.color.getRgb()

    def getRgbLine(self):
        return self.colorLine.getRgb()

    def setRgb(self, rgb):
        tmp_rgb = rgb.strip('")("').strip('\')(\'').strip(')(').split(', ')

        self.color.setRgb(int(tmp_rgb[0]), int(tmp_rgb[1]), int(tmp_rgb[2]), alpha = int(tmp_rgb[3]) )

        self.update(self.color)

    def setRgbLine(self, rgb):
        tmp_rgb = rgb.strip('")("').strip('\')(\'').strip(')(').split(', ')

        self.colorLine.setRgb(int(tmp_rgb[0]), int(tmp_rgb[1]), int(tmp_rgb[2]), alpha = int(tmp_rgb[3]) )

        self.updateLine(self.colorLine)

    def updateLine(self, color):
        self.lineStyleColorBotton.setStyleSheet(CONSTANTS.COLOR_TEXT.format(rgb = color.name()))
        self.colorLine = color

    def update(self, color):
        self.colorButton.setStyleSheet(CONSTANTS.COLOR_TEXT.format(rgb = color.name()))
        self.color = color