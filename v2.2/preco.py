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

xl = pd.ExcelFile("Café Contrato C Futuros Dados Históricos - Semanal.xlsx")
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
cftc['Percentil_Especulador'] = percentil1.T
#percentil1 = pd.Series(percentil1[:,0], index=np.arange(0,432,1))

produtor1=cftc.Prod_Merc_Positions_Long_ALL
produtor2=cftc.Prod_Merc_Positions_Short_ALL
y2 = produtor1-produtor2
y2_norm = normalizar(y2)
percentil2 = calcular_percentil(y2_norm)
cftc['Percentil_Produtor'] = percentil2.T  
#percentil2 = pd.Series(percentil2[:,0], index= np.arange(0,432,1))

outros1=cftc.Other_Rept_Positions_Long_ALL
outros2=cftc.Other_Rept_Positions_Short_ALL
y3 = outros1-outros2
y3_norm = normalizar(y3)
percentil3 = calcular_percentil(y3_norm)
cftc['Percentil_Outros'] = percentil3.T   
#percentil3 = pd.Series(percentil3[:,0], index= np.arange(0,432,1))

#Cálculo das médias móveis
precos['Médias_Móveis'] = precos['Último'].sort_index(ascending=False).rolling(window=4).mean().sort_index(ascending=True)

cftc['Médias_Móveis_Especulador'] = cftc['Percentil_Especulador'].sort_index(ascending=False).rolling(window=3).mean().sort_index(ascending=True)
cftc['Médias_Móveis_Produtor'] = cftc['Percentil_Produtor'].sort_index(ascending=False).rolling(window=3).mean().sort_index(ascending=True)
cftc['Médias_Móveis_Outros'] = cftc['Percentil_Outros'].sort_index(ascending=False).rolling(window=3).mean().sort_index(ascending=True)

trace_precos = go.Candlestick(x = precos.Data,
    open=precos.Abertura,
    high=precos.Máxima,
    low=precos.Mínima,
    close=precos.Último,
#    mode = 'lines',
    name = 'Preços',
    increasing=dict(line=dict(color= '#17BECF')),
    decreasing=dict(line=dict(color= '#7F7F7F'))
    )
    
trace_medias_moveis = go.Scatter(
    x = precos.Data,
    y = precos.Médias_Móveis,
    visible = 'legendonly',
    mode = 'lines',
    name = 'Médias Móveis - Preços',
    line = dict(
        color = ('#E377C2'),
        width = 2)
    )
        
trace_especulador = go.Scatter(
    x = cftc.Date,
    y = percentil1*100,
    mode = 'lines',
    name = 'Especulador',
    line = dict(
        color = ('#649FF4'),
        width = 2)
    )
trace_mediasmoveis_especulador = go.Scatter(
    x = cftc.Date,
    y = cftc.Médias_Móveis_Especulador*100,
    mode = 'lines',
    visible = 'legendonly',
    name = 'Médias Móveis - Especulador',
    line = dict(
        color = ('#A4C2F4'),
        width = 2)
    )
        
trace_produtor = go.Scatter(
    x = cftc.Date,
    y = percentil2*100,
    mode = 'lines',
    name = 'Produtor',
    line = dict(
        color = ('#54C9CF'),
        width = 2)
    )

trace_mediasmoveis_produtor = go.Scatter(
    x = cftc.Date,
    y = cftc.Médias_Móveis_Produtor*100,
    mode = 'lines',
    visible = 'legendonly',
    name = 'Médias Móveis - Produtor',
    line = dict(
        color = ('#9ACECF'),
        width = 2)
    )
        
trace_outros = go.Scatter(
    x = cftc.Date,
    y = percentil3*100,
    mode = 'lines',
    name = 'Outros',
    line = dict(
        color = ('#CC9A88'),
        width = 2
         )
    )

trace_mediasmoveis_outros = go.Scatter(
    x = cftc.Date,
    y = cftc.Médias_Móveis_Outros*100,
    visible = 'legendonly',
    mode = 'lines',
    name = 'Médias Móveis - Outros',
    line = dict(
        color = ('#CCC'),
        width = 2)
    )
        
rangeselector=dict(
#    visibe = True,
    x = 0, y = 1,
    bgcolor = 'rgba(150, 200, 250, 0.4)',
    font = dict( size = 13 ),
    buttons=list([
#        dict(count=1,
#             label='Resetar',
#             step='all'),
        dict(count=1,
             label='1 ano',
             step='year',
             stepmode='backward'),
        dict(count=3,
            label='3 meses',
            step='month',
            stepmode='backward'),
        dict(count=1,
            label='1 mês',
            step='month',
            stepmode='backward'),
        dict(label='Tudo',
            step='all')
    ]))
            
fig = tools.make_subplots(rows=2, cols=1, subplot_titles=('Histórico de Preços - Café Contrato C Futuros', 'CFTC'))

fig['layout']['xaxis']['rangeselector'] = rangeselector
fig['layout']['plot_bgcolor'] = 'rgb(250, 250, 250)'

fig.append_trace(trace_precos, 1, 1)
fig.append_trace(trace_medias_moveis, 1, 1)
fig.append_trace(trace_especulador, 2, 1)
fig.append_trace(trace_produtor, 2, 1)
fig.append_trace(trace_outros, 2, 1)
fig.append_trace(trace_mediasmoveis_especulador, 2, 1)
fig.append_trace(trace_mediasmoveis_produtor, 2, 1)
fig.append_trace(trace_mediasmoveis_outros, 2, 1)

fig['layout'].update(height=1000, width=1500, title='Análise do Comportamento do Mercado de Commodities')
py.plot(fig, filename='AgroRenda.html')
#fig_comp = go.Figure(data=data_comp, layout=layout_comp)
#py.plot(fig_comp)