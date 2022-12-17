import plotly.graph_objects as go

class line_chart:

    args = [
        'name',
        # 'visible',
        # 'showlegend',
        # 'legendrank'
    ]

    @staticmethod
    def create_figure():
        return go.Figure()

    @staticmethod
    def add_trace(fig, x, y, args):
        return fig.add_trace(
            go.Scatter(
                x=x, 
                y=y,
                **args
            )
        )