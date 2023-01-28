import plotly.graph_objects as go

# Data for the chart
x = ['Apples', 'Bananas', 'Oranges']
y = [3, 2, 4]

# Create the chart
fig = go.Figure(data=[go.Bar(x=x, y=y, hoverinfo='y+x+z+all')])

# Show the chart
fig.show()
