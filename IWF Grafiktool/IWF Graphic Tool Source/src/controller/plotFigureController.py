from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from qtpy import QtWidgets, QtGui

#this has to be imported even though it isn't used directly, otherwise the EXE won't save images
import matplotlib.backends.backend_ps
import matplotlib.backends.backend_pdf
import matplotlib.backends.backend_pgf
import matplotlib.backends.backend_agg
import matplotlib.backends.backend_svg

from misc.constants import *

class PlotFigureController:
    def __init__(self, application):
        self.application = application
        self.mainUi = application.mainUi

        self.figure = Figure()

    def create_figure(self):
        self.figure = Figure(figsize=(self.mainUi.imageWidth.value()*CM, self.mainUi.imageHeight.value()*CM))

    def repaint_figure(self):
        """
        We draw a new figure over the current figure to prevent a flicker effect.

        After redrawing, the previous figure will be removed.
        """    
        canvas = FigureCanvas(self.figure)
        self.application.scene.addWidget(canvas)

        for item in self.application.scene.items():
            if item.widget() != canvas:
                item.deleteLater()

    def validate_user_text_input(self):
        fig = Figure()
        ax = fig.gca()
        txt_to_check = ''
        for widget in self.application.widgets:
            if isinstance(widget, QtWidgets.QPlainTextEdit):
                txt_to_check += widget.toPlainText()
            elif isinstance(widget, QtWidgets.QLineEdit):
                txt_to_check += widget.text()
        ax.text(0, 0, txt_to_check)
        try:
            fig.savefig('cache/tmp.png')
        except ValueError:
            raise ValueError('Invalides LaTex...')
        self.enable()

    def disable(self):
        self.application.scene.setForegroundBrush(QtGui.QColor(MAX_RGB_VALUE, MAX_RGB_VALUE, MAX_RGB_VALUE, INVALID_FIGURE_ALPHA))
    def enable(self):
        self.application.scene.setForegroundBrush(QtGui.QColor(MAX_RGB_VALUE, MAX_RGB_VALUE, MAX_RGB_VALUE, 0))