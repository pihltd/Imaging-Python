import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

app = dash.Dash()
#data = [4500,2500,1053,500]
#labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    dcc.Graph( id='Graph', 
        figure = {
        'data' : [
            go.Pie(values=[4500,2500,1053,500],  labels=['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen'])
        ]
        }
        )

    #dcc.Graph(
     #   id='example-graph',
        #figure={
#            'data': [
  #              {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
    #            {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montreal'},
      #      ],
        #    'layout': {
#                'title': 'Dash Data Visualization'
#            }
#        }
#    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
