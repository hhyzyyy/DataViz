import IWF_template_modify
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
import pandas as pd

from MyUtils import utils
from pylatexenc.latex2text import LatexNodes2Text
from pylatexenc.latexencode import unicode_to_latex


print(3*3.7795275590551)

# utils.modify_logo("output/add_std.html")

# df = pd.read_excel("input/Axial WAIS.xlsx", header=1)
#
# group = df.groupby("PtType")
# mean = group.agg('mean')["Mittlere Kerbtiefe tm"]
# std = group.agg('std')["Mittlere Kerbtiefe tm"]
#
# df['avg_Kerbtiefe'] = df.groupby('PtType')['Mittlere Kerbtiefe tm'].transform('mean')
# df['std_Kerbtiefe'] = df.groupby('PtType')['Mittlere Kerbtiefe tm'].transform('std')
#
# # print(df["avg_Kerbtiefe"], df["std_Kerbtiefe"])
#
# x = [name for name,_ in group]
# # fig = px.scatter(
# #     df,
# #     x="PtType",
# #     y="avg_Kerbtiefe",
# #     error_y="std_Kerbtiefe",
# #     hover_data={"PtType": False}
# # )
#
# fig = px.scatter(
#     x=[0, 1, 2],
#     y=[6, 10, 2],
# )
#
# fig.update_traces(error_y=dict(
#             type='data', # value of error bar given in data coordinates
#             array=[3, 2, 10],
#             visible=True), selector=dict(type='scatter')
# )
# fig.show()


