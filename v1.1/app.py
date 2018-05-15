import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
#import plotly.graph_objs as go
#import plotly.offline as py

app = dash.Dash()

xl = pd.ExcelFile("CFTC.xlsx")
xl.sheet_names
[u'CFTC']
dataset = xl.parse("CFTC")
dataset.head()

#x=dataset.Date

def normalizar(x):
        x_min = min(x)
        x_max = max(x)
        return (x-x_min)/(x_max-x_min)

#def percentil(x):
#    count = 0
#    step = 52
#    for i in range(step):
#        if x>=x[i+1]:
#            count += 1
#    return count/step

y_total = dataset.Open_Interest_All

especulador1=dataset.M_Money_Positions_Long_ALL
especulador2=dataset.M_Money_Positions_Short_ALL
y1 = especulador1-especulador2
y1_norm = normalizar(y1)

#passo = 52
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
#colors = {
#    'background': '#1D0C67',
#    'text': '#7FDBFF'
#}

app.layout = html.Div(children=[
        html.H1('AgroRenda'),
        dcc.Checklist(
        options=[
        {'label': 'Especulador', 'value': 'Esp'},
        {'label': 'Produtor', 'value': 'Prod'},
        {'label': 'Outros', 'value': 'Out'}
                ],
    values=['Esp', 'Prod', 'Out'],
#    multi = True
                    ),  
        dcc.Graph(id='Posição Relativa - Traders', 
                  figure ={
                          'data':[
                                  {'x':dataset.Date, 'y':percentil1*100, 'type':'line', 'name':'Especulador'},
                                  {'x':dataset.Date, 'y':percentil2*100, 'type':'line', 'name':'Produtor'},
                                  {'x':dataset.Date, 'y':percentil3*100, 'type':'line', 'name':'Outros'},
                                  ],
                                  'layout':{ 
#                                           'plot_bgcolor': colors['background'],
#                                           'paper_bgcolor': colors['background'],
                                          'title': 'Posição Relativa - Traders'
                                          }
                                  })
        ])
    

if __name__ == '__main__':
    app.run_server(debug=True)    
   