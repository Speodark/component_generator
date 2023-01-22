import plotly.graph_objects as go

# Create data for the chart
x = ['A', 'B', 'C', 'D']
y = [1, 2, 3, 4]

# Create the bar chart
fig = go.Figure(data=[go.Bar(x=x, y=y, width=['0.4','1'])])

# Show the chart
fig.show()
