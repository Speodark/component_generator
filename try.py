import plotly.graph_objects as go
import json

# Data for the bar chart
x = ['apples', 'oranges', 'bananas']
y = [3, 4, 2]

# Create the bar chart
json_data = go.Bar(x=x, y=y).to_plotly_json()

print(json_data)

fig = go.Figure([json_data,json_data])
print(fig)
fig.show()