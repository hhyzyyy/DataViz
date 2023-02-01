from misc.constants import *

class PlotLegendController:
    def __init__(self, application):
        self.application  = application
        self.mainUi = application.mainUi

    def get_legend_texts(self, main = True):
        if main:
            return self._get_legends(self.mainUi.legend.toPlainText())
        return self._get_legends(self.mainUi.legend2.toPlainText())

    def _get_legends(self, textField):
        legends = ['']*PLOT_ELEMENT_SIZE
        for idx, val in enumerate(textField.strip().split('\n\n')):
            if idx >= PLOT_ELEMENT_SIZE:
                break
            legends[idx] = MATHMODE_NO_SPACE + val + MATHMODE_NO_SPACE
        return legends

    def handle_legends(self):
        if self.mainUi.disableLegend.isChecked() and (self.application.axesController.yAxis.data.shape[0] > 0):
            leg = self.application.axesController.axes.legend(
                loc=(self.mainUi.paddingLeftLegend.value()/self.mainUi.width.value(), self.mainUi.paddingTopLegend.value()/self.mainUi.height.value()), 
                framealpha=self.mainUi.legendFrameAlpha.value(), 
                frameon=self.mainUi.disableLegendFrame.isChecked(),
                borderpad=self.mainUi.legendFramePad.value(),
                handletextpad=self.mainUi.legendTextPad.value(), 
                labelspacing =self.mainUi.legendSpacing.value(),
                handlelength = self.mainUi.handlelength.value(),
                handleheight = self.mainUi.handleheight.value(),
                ncol = int(self.mainUi.legendTextCol.value()),
                fancybox = False,
                columnspacing = self.mainUi.legendColumnSpacing.value(),
                scatteryoffsets=[self.mainUi.legendScatterOffset.value()])
            leg.set_zorder(500)
            leg.get_frame().set_edgecolor('k')
            leg.get_frame().set_linewidth(self.mainUi.legendFrameWidth.value())

        if self.mainUi.disableLegend.isChecked() and self.application.dataHandler.has_second_axes():
            leg = self.application.axesController.twinAxes.legend(
                loc=(self.mainUi.paddingLeftLegend_2.value()/self.mainUi.width.value(), self.mainUi.paddingTopLegend_2.value()/self.mainUi.height.value()), 
                framealpha=self.mainUi.legendFrameAlpha_2.value(), 
                frameon=self.mainUi.disableLegendFrame_2.isChecked(),
                borderpad=self.mainUi.legendFramePad_2.value(),
                handletextpad=self.mainUi.legendTextPad_2.value(), 
                labelspacing =self.mainUi.legendSpacing_2.value(),
                handlelength = self.mainUi.handlelength_2.value(),
                handleheight = self.mainUi.handleheight_2.value(),
                ncol = int(self.mainUi.legendTextCol_2.value()),
                fancybox = False,
                columnspacing = self.mainUi.legendColumnSpacing_2.value(),
                scatteryoffsets=[self.mainUi.legendScatterOffset_2.value()])
            leg.set_zorder(500)
            leg.get_frame().set_edgecolor('k')
            leg.get_frame().set_linewidth(self.mainUi.legendFrameWidth_2.value())