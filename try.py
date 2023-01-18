import plotly.graph_objects as go

# Create some data
x = ["A", "B", "C", "D"]
y1 = [1, 2, 3, 4]
y2 = [-2, -1, 0, 1]

# Create the bar chart
fig = go.Figure(data=[go.Bar(x=x, y=y1, name="y1", base=0),
                     go.Bar(x=x, y=y2, name="y2", base=-5)])
fig.update_layout(
    xaxis=dict(title='X axis'),
    yaxis=dict(title='Y axis'),
    barmode='group'
)
fig.show()
