import plotly.graph_objects as go
import plotly.io as pio

pio.templates["IWF_template_raw"] = go.layout.Template()
IWF_template_raw = pio.templates["IWF_template_raw"]


# General constants
Font = dict(family='Arial', size=14, color='black')

axis_layout = dict(showline=True, linewidth=1.5, linecolor='black',
                   gridcolor='black', gridwidth=1,
                   zeroline=True, zerolinewidth=1.5, zerolinecolor='black',
                   ticks="outside", tickcolor='rgba(0 ,0, 0, 0)', ticklen=7, tickwidth=0.1,
                   titlefont=Font
                   )


# Colors
# categorical Colors
iwfColors_ohneWeiß = ['black', 'rgb(159, 182, 196)', 'rgb(125, 102, 102)', 'rgb(153, 0, 0)']
FraunhoferColors = ['rgb(0, 152, 121)', 'rgb(0, 153, 178)', 'rgb(67, 105, 123)', 'rgb(97, 101, 103)',
                    'rgb(147, 151, 153)', 'rgb(199, 201, 202)']
PTZ_colores = iwfColors_ohneWeiß + FraunhoferColors

IWF_template_raw.data.scatter = [go.Scatter(marker=dict(symbol="circle", size=8, color=PTZ_colores[0])),
                                 go.Scatter(marker=dict(symbol="square", size=8, color=PTZ_colores[1])),
                                 go.Scatter(marker=dict(symbol="diamond", size=8, color=PTZ_colores[2])),
                                 go.Scatter(marker=dict(symbol="triangle-up", size=8, color=PTZ_colores[3])),
                                 go.Scatter(marker=dict(symbol="triangle-down", size=8, color=PTZ_colores[4])),
                                 go.Scatter(marker=dict(symbol="cross", size=8, color=PTZ_colores[5])),
                                 go.Scatter(marker=dict(symbol="x", size=8, color=PTZ_colores[6]))]

# sequential colors
IWF_Red_Fade = ['#ffe6e6', '#990000', ]
IWF_GreyBlue_fade = ['#dfe7ec', '#9fb6c4', '#3a515f']
IWF_Brown_fade = ['#e8e3e3', '#7d6666', '#382e2e']
IWF_Black_fade = ['#f2f2f2', '#000000']



# layout


IWF_template_raw.layout = dict(
    font=Font,
    title=dict(font=Font),
    legend=dict(font=Font),
    plot_bgcolor='white',
    xaxis=axis_layout,
    yaxis=axis_layout,
    # margin=dict(l=10, r=10, b=10, t=30, pad=0),  # Default Margins
    # width=1000, height=600                       # Default Graph Size
)
IWF_template_raw.layout.shapes = [
    dict(name='black_frame', type="rect", xref="paper", yref="paper", x0=0, y0=0, x1=1.0, y1=1.0,
         line=dict(color="black", width=1))]

IWF_template_raw.layout.colorway = PTZ_colores
IWF_template_raw.layout.colorscale.sequential = IWF_Red_Fade




# Data
IWF_template_raw.data.scatter = [dict(hovertemplate=r": %{x} %{text} <extra></extra>")]



# Setting Template
modebar = dict({
    'scrollZoom': True,
    'displaylogo': False,
    'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
    'toImageButtonOptions': {'format': 'png',  # one of png, svg, jpeg, webp
                             'filename': 'Zwischengespeicherter_Plot', }
})

pio.templates["IWF_template_modify"] = 'plotly+IWF_template_raw'
pio.templates.default = "IWF_template_modify"


