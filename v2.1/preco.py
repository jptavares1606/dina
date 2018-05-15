# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 14:34:25 2018

@author: jptav
"""
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.offline as py
from plotly import tools

xl = pd.ExcelFile("CFTC.xlsx")
xl.sheet_names
[u'CFTC']
cftc = xl.parse("CFTC")
cftc.head()

xl = pd.ExcelFile("Café Contrato C Futuros Dados Históricos - Diário.xlsx")
xl.sheet_names
[u'Preços']
precos = xl.parse("Preços")
precos.head()
precos['Data'] = pd.to_datetime(precos['Data'], format='%d.%m.%Y')

def normalizar(x):
        x_min = min(x)
        x_max = max(x)
        return (x-x_min)/(x_max-x_min)

def calcular_percentil(norm):
    count = 0
    length = len(norm)
    percentil = np.zeros((1,length))

    for j in range(length):
        for i in range(length):
            if norm[j]>=norm[i]:
                count += 1
        percentil[0,j] = count/length
        count = 0
    return percentil[0,:]
    
y_total = cftc.Open_Interest_All

especulador1=cftc.M_Money_Positions_Long_ALL
especulador2=cftc.M_Money_Positions_Short_ALL
y1 = especulador1-especulador2
y1_norm = normalizar(y1)
percentil1 = calcular_percentil(y1_norm)
percentil1 = percentil1.T
#percentil1 = pd.Series(percentil1[:,0], index=np.arange(0,432,1))

produtor1=cftc.Prod_Merc_Positions_Long_ALL
produtor2=cftc.Prod_Merc_Positions_Short_ALL
y2 = produtor1-produtor2
y2_norm = normalizar(y2)
percentil2 = calcular_percentil(y2_norm)
percentil2 = percentil2.T   
#percentil2 = pd.Series(percentil2[:,0], index= np.arange(0,432,1))

outros1=cftc.Other_Rept_Positions_Long_ALL
outros2=cftc.Other_Rept_Positions_Short_ALL
y3 = outros1-outros2
y3_norm = normalizar(y3)
percentil3 = calcular_percentil(y3_norm)
percentil3 = percentil3.T 
#percentil3 = pd.Series(percentil3[:,0], index= np.arange(0,432,1))

#Cálculo das médias móveis
precos['Médias_Móveis'] = precos['Último'].rolling(window=30).mean()

trace_especulador = go.Scatter(
    x = cftc.Date,
    y = percentil1*100,
    mode = 'lines',
    name = 'Especulador',
    line = dict(
        color = ('#2200FF'),
        width = 2)
    )

trace_produtor = go.Scatter(
    x = cftc.Date,
    y = percentil2*100,
    mode = 'lines',
    name = 'Produtor',
    line = dict(
        color = ('#FF0000'),
        width = 2)
    )

trace_outros = go.Scatter(
    x = cftc.Date,
    y = percentil3*100,
    mode = 'lines',
    name = 'Outros',
    line = dict(
        color = ('#18FFBA'),
        width = 2
         )
    )

trace_precos = go.Scatter(
    x = precos.Data,
    y = precos.Último,
    mode = 'lines',
    name = 'Preços',
    line = dict(
        color = ('#2200FF'),
        width = 2)
    )

trace_medias_moveis = go.Scatter(
    x = precos.Data,
    y = precos.Médias_Móveis,
    mode = 'lines',
    name = 'Média Móvel',
    line = dict(
        color = ('#FF0000'),
        width = 2)
    )
    

#data_cftc = [trace_especulador, trace_produtor, trace_outros]
#layout_comp = go.Layout(
#    title='Posição Relativa x Data (CFTC)',
#    hovermode='closest',
#    xaxis=dict(
#        title='Data',
#        ticklen=5,
#        zeroline=False,
#        gridwidth=2,
#    ),
#    yaxis=dict(
#        title='Posição Relativa (%)',
#        ticklen=5,
#        gridwidth=2,
#    ),
#)
#
#data_preco = [trace_precos]
#layout_comp = go.Layout(
#    title='Histórico de Preços - Café Contrato C Futuros',
#    hovermode='closest',
#    xaxis=dict(
#        title='Data',
#        ticklen=5,
#        zeroline=False,
#        gridwidth=2,
#    ),
#    yaxis=dict(
#        title='Preço (Dólar por libra peso)',
#        ticklen=5,
#        gridwidth=2,
#    ),
#)
    
fig = tools.make_subplots(rows=2, cols=1, subplot_titles=('Histórico de Preços - Café Contrato C Futuros', 'CFTC'))

fig.append_trace(trace_precos, 1, 1)
fig.append_trace(trace_medias_moveis, 1, 1)
fig.append_trace(trace_especulador, 2, 1)
fig.append_trace(trace_produtor, 2, 1)
fig.append_trace(trace_outros, 2, 1)

fig['layout'].update(height=1000, width=1500, title='Análise do Comportamento do Mercado de Commodities')
py.plot(fig, filename='AgroRenda.html')
#fig_comp = go.Figure(data=data_comp, layout=layout_comp)
#py.plot(fig_comp)