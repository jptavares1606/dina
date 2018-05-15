import pandas as pd
import plotly.graph_objs as go
import plotly.offline as py


xl = pd.ExcelFile("CFTC.xlsx")
xl.sheet_names
[u'CFTC']
dataset = xl.parse("CFTC")
dataset.head()

x=dataset.Date

especulador1=dataset.M_Money_Positions_Long_ALL
especulador2=dataset.M_Money_Positions_Short_ALL
y1 = abs(especulador1-especulador2)

produtor1=dataset.Prod_Merc_Positions_Long_ALL
produtor2=dataset.Prod_Merc_Positions_Short_ALL
y2 = abs(produtor1-produtor2)

outros1=dataset.Other_Rept_Positions_Long_ALL
outros2=dataset.Other_Rept_Positions_Short_ALL
y3 = abs(outros1-outros2)

y_total = dataset.Open_Interest_All

trace_especulador = go.Scatter(
    x = x,
    y = y1/y_total,
    mode = 'lines',
    name = 'Especulador')

trace_produtor = go.Scatter(
    x = x,
    y = y2/y_total,
    mode = 'lines',
    name = 'Produtor')

trace_outros = go.Scatter(
    x = x,
    y = y3/y_total,
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