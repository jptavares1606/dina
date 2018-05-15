# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 14:34:25 2018

@author: jptav
"""
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.offline as py

xl = pd.ExcelFile("CFTC.xlsx")
xl.sheet_names
[u'CFTC']
dataset = xl.parse("CFTC")
dataset.head()

def normalizar(x):
        x_min = min(x)
        x_max = max(x)
        return (x-x_min)/(x_max-x_min)

y_total = dataset.Open_Interest_All

especulador1=dataset.M_Money_Positions_Long_ALL
especulador2=dataset.M_Money_Positions_Short_ALL
y1 = especulador1-especulador2
y1_norm = normalizar(y1)
count1 = 0
y1_length = len(y1_norm)
percentil1 = np.zeros((1,y1_length))

for j in range(y1_length):
    for i in range(y1_length):
        if y1_norm[j]>=y1_norm[i]:
            count1 += 1
    percentil1[0,j] = count1/y1_length
    count1 = 0
percentil1 = percentil1.T
percentil1 = pd.Series(percentil1[:,0], index= np.arange(0,432,1))

produtor1=dataset.Prod_Merc_Positions_Long_ALL
produtor2=dataset.Prod_Merc_Positions_Short_ALL
y2 = produtor1-produtor2
y2_norm = normalizar(y2)
count2 = 0
y2_length = len(y2_norm)
percentil2 = np.zeros((1,y2_length))

for j in range(y2_length):
    for i in range(y2_length):
        if y2_norm[j]>=y2_norm[i]:
            count2 += 1
    percentil2[0,j] = count2/y2_length
    count2 = 0
percentil2 = percentil2.T   
percentil2 = pd.Series(percentil2[:,0], index= np.arange(0,432,1))

outros1=dataset.Other_Rept_Positions_Long_ALL
outros2=dataset.Other_Rept_Positions_Short_ALL
y3 = outros1-outros2
y3_norm = normalizar(y3)
count3 = 0
y3_length = len(y3_norm)
percentil3 = np.zeros((1,y3_length))

for j in range(y3_length):
    for i in range(y3_length):
        if y3_norm[j]>=y3_norm[i]:
            count3 += 1
    percentil3[0,j] = count3/y3_length
    count3 = 0
percentil3 = percentil3.T 
percentil3 = pd.Series(percentil3[:,0], index= np.arange(0,432,1))

trace_especulador = go.Scatter(
    x = dataset.Date,
    y = percentil1*100,
    mode = 'lines',
    name = 'Especulador')

trace_produtor = go.Scatter(
    x = dataset.Date,
    y = percentil2*100,
    mode = 'lines',
    name = 'Produtor')

trace_outros = go.Scatter(
    x = dataset.Date,
    y = percentil3*100,
    mode = 'lines',
    name = 'Outros')

data_comp = [trace_especulador, trace_produtor, trace_outros]
layout_comp = go.Layout(
    title='Posição Relativa x Data (CFTC)',
    hovermode='closest',
    xaxis=dict(
        title='Data',
        ticklen=5,
        zeroline=False,
        gridwidth=2,
    ),
    yaxis=dict(
        title='Posição Relativa (%)',
        ticklen=5,
        gridwidth=2,
    ),
)
fig_comp = go.Figure(data=data_comp, layout=layout_comp)
py.plot(fig_comp)