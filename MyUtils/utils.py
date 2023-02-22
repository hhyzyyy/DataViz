# -*- coding: utf-8 -*-
"""
   Author:  Huayu Hu
   Contact: huayu.hu@outlook.com
   Date:    2022/11/21
"""
import os
import re
import numpy as np
import yaml

from bs4 import BeautifulSoup
from pylatexenc.latex2text import LatexNodes2Text
from queue import PriorityQueue

abspath = os.path.abspath(__file__)

 
def read_config():
    path = abspath.replace("utils.py", "misc/config.yaml")
    with open(path, "r", errors='ignore') as fs:
        yaml_data = yaml.load(fs, Loader=yaml.FullLoader)
    return yaml_data


def get_tickvals_ticktext(start, end, step, unit):
    tickvals = np.arange(start, end + step, step)
    if len(tickvals) < 2:
        raise Exception(
            f"[WARNING]: Please change the range of x or y to ensure that at least two scales exist: {tickvals}")
    ticktext = list(tickvals).copy()
    if unit is not None:
        ticktext[-2] = unit
    return tickvals, ticktext


def add_unit(fig, x=None, x_unit=None, y=None, y_unit=None):
    """
    Add units to the penultimate scale of the x-axis or y-axis
    """
    if x is not None and len(x) == 3 and y is not None and len(y) == 3:
        x_tickvals, x_ticktext = get_tickvals_ticktext(x[0], x[1], x[2], x_unit)
        y_tickvals, y_ticktext = get_tickvals_ticktext(y[0], y[1], y[2], y_unit)
        fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=x_tickvals,
                ticktext=x_ticktext
            ),
            yaxis=dict(
                tickmode='array',
                tickvals=y_tickvals,
                ticktext=y_ticktext
            )
        )
        fig = update_hover(fig, x_unit)
        fig = resize_window(fig, x_range=x[:2], y_range=y[:2])
        return fig


def handle_latex(latex):
    """
    Convert Latex to Unicode
    """
    unit = LatexNodes2Text().latex_to_text(latex)
    sup = re.findall(r"\^{[^}]+}", latex)
    sub = re.findall(r"_{[^}]+}", latex)

    for sp in sup:
        elm = sp.replace("^", "").replace("{", "").replace("}", "")
        text = ""
        for c in elm:
            unicode = superscript[character.index(c)]
            if unicode == "!":
                raise Exception(f"No superscript of {c} exists.")
            text += unicode
        unit = unit.replace("^" + elm, text, 1)

    for sb in sub:
        elm = sb.replace("_", "").replace("{", "").replace("}", "")
        text = ""
        for c in elm:
            unicode = subscript[character.index(c)]
            if unicode == "!":
                raise Exception(f"No subscript of {c} exists.")
            text += unicode
        unit = unit.replace("_" + elm, text, 1)

    return unit


def update_hover(fig, x_unit=None, y_unit=None):
    # x_units = handle_latex(x_unit)
    # print(x_units)
    # y_units = handle_latex(y_unit)

    q = PriorityQueue()
    # Use the priority queue to get the maximum value
    for i in range(len(fig.data)):
        q.put(len(fig.data[i]["x"]))

    fig.update_traces(
        text=[x_unit for _ in range(q.queue[-1])],
        hovertemplate=fig.layout["xaxis"]["title"]["text"] + r": %{x} %{text} <extra></extra>",
    )
    return fig


character = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-=()"
superscript = "ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖ!ʳˢᵗᵘᵛʷˣʸᶻᴬᴮᒼᴰᴱ!ᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾ!ᴿᣵᵀᵁᘁᵂᕽᵞᙆ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾"
subscript = "ₐ!!!ₑ!!ₕ!!ₖₗₘₙₒₚ!!ₛₜ!!!ₓ!!!!!!!!!!!!!!!!!!!!!!!!!!!!₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎"


def resize_figure(fig, width, height):
    """ The units of width and height are mm """
    mm_px_ratio = 3.7795275590551  # 1 mm = 3.7795275590551 px
    fig.update_layout(
        width=width * mm_px_ratio,
        height=height * mm_px_ratio
    )
    return fig


def modify_logo(image_path, logo="TU_Berlin_logo", href=None, hover_text=None):
    plotly_logo = read_config()["plotly_logo"]
    default_logo = plotly_logo["default_logo"]

    if href is None:
        href = plotly_logo["href"]
    if hover_text is None:
        hover_text = plotly_logo["hover_text"]
    new_logo = (plotly_logo[logo])

    with open(image_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    soup = str(soup).replace("https://plotly.com/", href)
    soup = soup.replace('(this.graphInfo,"Produced with Plotly.js")', f'(this.graphInfo,"{hover_text}")')
    soup = soup.replace(default_logo, new_logo)

    new_image = os.path.splitext(image_path)[0] + f"_{logo}" + ".html"
    with open(new_image, "w") as f:
        f.write(soup)


def resize_window(fig, x_range=None, y_range=None):
    fig.update_xaxes(range=x_range)
    fig.update_yaxes(range=y_range)
    return fig

# def get_error(x, error_y, sort):
#     if error_y is not None:
#         dt = {}  # Coordinates and standard deviations correspond to each other
#         if sort:
#             for i, v in enumerate(np.sort(np.unique(x))):
#                 dt[v] = list(error_y)[i]
#         else:
#             for i, v in enumerate(x):
#                 dt[v] = list(error_y)[i]
#
#         error = []
#         v = x[0]
#         count = 0
#         for elm in x:
#             if elm != v:
#                 error.extend([dt[v]] * count)
#                 v = elm
#                 count = 0
#             count += 1
#         error.extend([dt[v]] * count)
#         return error
#
#
# def add_std(fig, error_y, sort=True):
#     """
#     Adding standard deviation to a scatter plot
#     """
#     data = fig.data
#     if len(data) > 1:  # Multiple Scatter Plot
#         for i, d in enumerate(data):
#             d["error_y"] = dict(
#                 type='data',  # value of error bar given in data coordinates
#                 array=error_y[i],
#                 visible=True,
#                 color="black"
#             )
#         fig.data = data
#     else:  # Single Scatter Plot
#         fig = fig.update_traces(
#             error_y=dict(
#                 type='data',
#                 array=get_error(data[0]["x"], error_y, sort),
#                 visible=True,
#                 color="black"
#             ),
#             selector=dict(type='scatter')
#         )
#     return fig
