"""
Callback structure written by chatGPT
This section defines a Dash callback, which is essential for the interactivity of the app.
Documenting this scheme is important because:
- It clarifies how input and output components are connected.
- It helps other developers understand the reactive logic of the UI.
- It serves as a reusable template for future functions in this project.
- It improves code maintainability and helps prevent bugs when modifying or scaling the app.
"""

from dash import Dash, Input, Output, State, html, dcc, callback

app = Dash(__name__)

app.layout = html.Div(
    [
        dcc.Input(id="input-id", type="text"),
        html.Button("Enviar", id="button-id", n_clicks=0),
        html.Div(id="output-id"),
    ]
)


# Callback function
@callback(
    Output(
        "output-id", "children"
    ),  # Salida (id del componente, propiedad a actualizar)
    Input(
        "button-id", "n_clicks"
    ),  # Entrada (id del componente, propiedad a monitorear)
    State(
        "input-id", "value"
    ),  # Estado opcional (para obtener valores sin activación directa)
)
def update_output(n_clicks, input_value):
    if n_clicks > 0:
        return f"Has escrito: {input_value}"
    return ""


if __name__ == "__main__":
    app.run(debug=True)
