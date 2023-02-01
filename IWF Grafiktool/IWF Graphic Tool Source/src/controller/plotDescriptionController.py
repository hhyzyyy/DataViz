from misc.constants import *
import misc.transform as trf

class PlotDescriptionController:
    def __init__(self, application):
        self.application = application
        self.mainUi = application.mainUi

    def handle_main_labels(self):
        if self.mainUi.disableLabels.isChecked():
            for idx, line in enumerate(self.mainUi.titleText.toPlainText().split('\n')):
                x_pos = self.mainUi.paddingLeftTitle.value()/self.mainUi.width.value()

                y_start = self.mainUi.paddingTopTitle.value()/self.mainUi.height.value()
                line_space = self.mainUi.lineSpacing.value()*self.mainUi.fontSize.value()/trf.get_linespace_factor(self.mainUi.lineSpacing.value())
                y_pos = y_start-idx*line_space

                self.application.axesController.axes.text(
                    x_pos, 
                    y_pos, 
                    MATHMODE_NO_SPACE + line,
                    verticalalignment = 'center', 
                    transform=self.application.axesController.axes.transAxes)