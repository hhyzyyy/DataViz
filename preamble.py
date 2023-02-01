import plotly.express as px, plotly.graph_objects as go
import pandas as pd, numpy as np


import IWF_template
import plotly.io as pio
pio.templates.default = "IWF_template"

modebar = dict({
    'scrollZoom': True,
    'displaylogo': False, 
    'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
    'toImageButtonOptions': {'format': 'png', # one of png, svg, jpeg, webp
    'filename': 'Zwischengespeicherter_Plot',}
})