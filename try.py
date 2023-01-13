import plotly.graph_objects as go

# Create a bar chart with two bars, grouped together in one legend item
trace1 = go.Bar(x=[1, 2], y=[10, 20], legendgroup='Group 1', name='Bar 1')
trace2 = go.Bar(x=[1, 2], y=[15, 25], legendgroup='Group 1', name='Bar 2',
legendgrouptitle={
    'font' : {
        'color' : '',
        'family' : 'Overpass',
        'size' : 20
    },
    'text' : 'hello'
}

)

data = [trace1, trace2]
layout = go.Layout(
    xaxis=dict(tickvals=[1, 2]),
    yaxis=dict(title='Value'),
)
fig = go.Figure(data=data, layout=layout)
fig.show()