import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly import tools
#import plotly.offline as py

app = dash.Dash()

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
percentil1 = percentil1.T
#percentil1 = pd.Series(percentil1[:,0], index= np.arange(0,432,1))
 
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
#colors = {
#    'background': '#1D0C67',
#    'text': '#7FDBFF'
#}
trace_especulador = go.Scatter(
    x = cftc.Date,
    y = percentil1*100,
    mode = 'lines',
    name = 'Especulador')

trace_produtor = go.Scatter(
    x = cftc.Date,
    y = percentil2*100,
    mode = 'lines',
    name = 'Produtor')

trace_outros = go.Scatter(
    x = cftc.Date,
    y = percentil3*100,
    mode = 'lines',
    name = 'Outros')

trace_precos = go.Scatter(
    x = precos.Data,
    y = precos.Último,
    mode = 'lines',
    name = 'Preços')
    
fig = tools.make_subplots(rows=2, cols=1)

fig.append_trace(trace_precos, 1, 1)
fig.append_trace(trace_especulador, 2, 1)
fig.append_trace(trace_produtor, 2, 1)
fig.append_trace(trace_outros, 2, 1)

fig['layout'].update(height=1000, width=1500, title='Análise do Comportamento do Mercado de Commodities')

app.layout = html.Div(children=[
        html.H1('AgroRenda'),
         dcc.Graph(figure=fig, id='my-figure')
#        dcc.Checklist(
#        options=[
#        {'label': 'Especulador', 'value': 'Esp'},
#        {'label': 'Produtor', 'value': 'Prod'},
#        {'label': 'Outros', 'value': 'Out'}
#                ],
#    values=['Esp', 'Prod', 'Out'],
#    multi = True
#                    ),  
#        dcc.Graph(id='Posição Relativa - Traders', 
#                  figure ={
#                          'data':[
#                                  {'x':cftc.Date, 'y':percentil1*100, 'type':'line', 'name':'Especulador'},
#                                  {'x':cftc.Date, 'y':percentil2*100, 'type':'line', 'name':'Produtor'},
#                                  {'x':cftc.Date, 'y':percentil3*100, 'type':'line', 'name':'Outros'},
#                                  ],
#                                  'layout':{ 
##                                           'plot_bgcolor': colors['background'],
##                                           'paper_bgcolor': colors['background'],
#                                          'title': 'Posição Relativa - Traders'
#                                          }
#                                  })
        ])
    
if __name__ == '__main__':
    app.run_server(debug=True)    
   