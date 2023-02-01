from misc.constants import *
import numpy as np
import misc.transform as trf

class IWFAxisElement:
    def __init__(
            self, 
            axes, 
            data = None,
            label = '', 
            label_position = '', 
            unit = '', 
            padding = 0, 
            decimals = 2, 
            rotation = 0, 
            outward = 0, 
            isMain = True, 
            isX = True, 
            isBarInFigure = False, 
            is_active = True, 
            parent_position = None):
        self.axes = axes
        self.data = data
        self.label = label
        self.label_position = label_position
        self.unit = unit
        self.padding = padding
        self.decimals = decimals
        self.rotation = rotation
        self.outward = outward
        self.isMain = isMain
        self.isX = isX
        self.isBarInFigure = isBarInFigure
        self.is_active = is_active
        self.parent_position = parent_position

    def calculate_ticks(self, baseAxe, twinAxe, mainUi, shareY):
        if self.isX:
            if self.isBarInFigure or not trf.is_float(self.data):
                self.xticks = np.arange(self.data.shape[0])
                self.xticksLabel = self.data.tolist()

                xmin = 0
                xmax = self.data.shape[0]
            else:
                tmp_x = self.data.astype(float)

                xmin = tmp_x.min()
                xmax = tmp_x.max()
                self.xticks = np.linspace(xmin, xmax, num = MAX_X_TICKS)
                self.xticksLabel = self.xticks

            self.axes.set_xlim(xmin, xmax)
        else:           
            if shareY:
                new_min = min(baseAxe.get_ylim()[0] + mainUi.yMinDoubleSpinBox.value(), twinAxe.get_ylim()[0]+mainUi.yMinDoubleSpinBox_2.value())
                new_max = max(baseAxe.get_ylim()[-1] + mainUi.yMaxDoubleSpinBox.value(), twinAxe.get_ylim()[1]+mainUi.yMaxDoubleSpinBox_2.value())
            else:
                if self.isMain:
                    new_min = self.axes.get_ylim()[0] + mainUi.yMinDoubleSpinBox.value() 
                    new_max = self.axes.get_ylim()[-1]+ mainUi.yMaxDoubleSpinBox.value()
                else:
                    new_min = self.axes.get_ylim()[0] + mainUi.yMinDoubleSpinBox_2.value()
                    new_max = self.axes.get_ylim()[-1] + mainUi.yMaxDoubleSpinBox_2.value()
            
            self.yticks = list(np.linspace(new_min, new_max, num = MAX_Y_TICKS))
            self.yticksLabel = self.yticks
            self.axes.set_ylim(new_min, new_max)  

    def handle_padding(self):
        if self.isX:
            self.axes.xaxis.labelpad = self.padding
        else:
            self.axes.yaxis.labelpad = self.padding

    def handle_ticks(self):
        if self.isX:
            self.axes.set_xticks(self.xticks)
            if self.isBarInFigure or not trf.is_float(self.data):
                self.axes.set_xticks(self.xticks + 0.5, minor=True)
        else:
            self.axes.set_yticks(self.yticks)

    def handle_rotation(self):
        if self.isX:
            for tick in self.axes.get_xticklabels(minor = False):
                tick.set_rotation(self.rotation)
            for tick in self.axes.get_xticklabels(minor = True):
                tick.set_rotation(self.rotation)
        else:
            for tick in self.axes.get_yticklabels():
                tick.set_rotation(self.rotation)

    def handle_position(self):
        if self.label_position == X_POSITION_TOP:
            self.axes.xaxis.tick_top()
            self.axes.xaxis.set_label_position(trf.spine_position(self.label_position))
        elif self.label_position == Y_POSITION_RIGHT:
            self.axes.yaxis.tick_right()
            self.axes.yaxis.set_label_position(trf.spine_position(self.label_position))

    def handle_outward(self, positions, width):
        if not self.isMain and positions.count(self.label_position) > 1:
            self.axes.spines[trf.spine_position(self.label_position)].set_position(('outward', self.outward))
            self.axes.spines[trf.spine_position(self.label_position)].set_visible(True)
            self.axes.spines[trf.spine_position(self.label_position)].set_linewidth(width)

    def handle_global_activation(self, numberFormat, lineSpacing):
        if self.is_active:
            self.add_axes_labels(numberFormat, lineSpacing)
        else:
            if self.isX:
                self.axes.set_xticklabels([])
            else:
                self.axes.set_yticklabels([])
            self.axes.spines[trf.spine_position(self.label_position)].set_position(('outward', 0))

    def add_axes_labels(self, numberFormat, lineSpacing):
        if self.isX:
            xtL = trf.list_to_float_locale(self.xticksLabel, numberFormat, int(self.decimals)) 
            if self.unit:
                xtL[UNIT_POSITION] = self.unit
            if self.isBarInFigure or not trf.is_float(self.data):
                self.axes.set_xticklabels(xtL, minor = True)
                self.axes.set_xticklabels('', minor = False)
            else:
                self.axes.set_xticklabels(xtL)
            self.axes.set_xlabel(MATHMODE_NO_SPACE + self.label + MATHMODE_NO_SPACE, linespacing=lineSpacing)
        else:
            ytL = trf.list_to_float_locale(self.yticksLabel, numberFormat, int(self.decimals))
            if self.unit:
                ytL[UNIT_POSITION] = self.unit
            self.axes.set_yticklabels(ytL)
            self.axes.set_ylabel(MATHMODE_NO_SPACE+ self.label + MATHMODE_NO_SPACE, linespacing=lineSpacing)

    def handle_tick_activation(self):
        if self.isMain:
            if self.isX:
                self.axes.xaxis.set_ticks_position('none')
            else:
                self.axes.yaxis.set_ticks_position('none')
        else:
            if self.isX and (self.parent_position != self.label_position or not self.is_active):
                self.axes.xaxis.set_ticks_position('none')
            elif not self.isX and (self.parent_position != self.label_position or not self.is_active):
                self.axes.yaxis.set_ticks_position('none')