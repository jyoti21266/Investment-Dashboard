import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import re

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title="Investment Dashboard"
)

app.layout = dmc.MantineProvider(
    children=dbc.Container([
        html.H2("Investment Dashboard", className="text-center my-4"),

        dbc.Row([
            dbc.Col([
                dbc.Label("Investment/Expense Category", className="fw-bold"),
                dcc.Dropdown(
                    id='idea-category-dropdown',
                    options=[
                        {'label': 'Improvement cum investment', 'value': 'improvement'},
                        {'label': 'Infrastructure development', 'value': 'infrastructure'},
                        {'label': 'Regulatory expenses', 'value': 'regulatory'},
                        {'label': 'Fixed cost related idea', 'value': 'fixed_cost'},
                    ],
                    placeholder="Select an Idea Category",
                    style={"width": "100%"}
                )
            ], width=6)
        ], className="mb-4"),

        html.Div(id='dynamic-container')
    ], fluid=True)
)

category_to_changes = {
    'infrastructure': ['Construction of road', 'Painting related work', 'Creating shed', 'Installing sewage pipeline', 'Others'],
    'regulatory': ['New audit', 'Compliance training', 'Others'],
    'fixed_cost': ['Salary increase', 'Others']
}

@app.callback(
    Output('dynamic-container', 'children'),
    Input('idea-category-dropdown', 'value')
)
def display_subcomponents(category):
    if not category:
        return None

    if category == 'improvement':
        lines = ['Pickling', '4-Hi Mill', 'ECL', 'BAF', 'SPM']
        return dbc.Row([
            dbc.Col([
                dbc.Label("Select the Line", className="fw-bold"),
                dcc.Dropdown(
                    id='line-dropdown',
                    options=[{'label': line, 'value': line} for line in lines],
                    placeholder="Select a process",
                    style={"width": "100%"}
                ),
                html.Br(),
                html.Div(id='line-change-dropdown-container'),
                html.Div(id='other-input-container')
            ], width=6)
        ])
    else:
        return dbc.Row([
            dbc.Col([
                dbc.Label("Reason for Investment/Expense", className="fw-bold"),
                dcc.Dropdown(
                    id='change-dropdown',
                    options=[{'label': item, 'value': item} for item in category_to_changes[category]],
                    placeholder="Select change type",
                    style={"width": "100%"}
                ),
                html.Br(),
                html.Div(id='other-input-container')
            ], width=6)
        ])


@app.callback(
    Output('line-change-dropdown-container', 'children'),
    Input('line-dropdown', 'value'),
    prevent_initial_call=True
)
def show_line_related_dropdown(selected_line):
    if selected_line and selected_line != 'Others':
        return html.Div([
            dbc.Label("Reason for investment/expense", className="fw-bold"),
            dcc.Dropdown(
                id='change-dropdown',
                options=[
                    {'label': 'Installation', 'value': 'Installation'},
                    {'label': 'Repair and Maintenance', 'value': 'Repair and Maintenance'},
                    {'label': 'Others', 'value': 'Others'}
                ],
                placeholder="Select change type",
                style={"width": "100%"}
            )
        ])
    return None


@app.callback(
    Output('other-input-container', 'children'),
    Input('change-dropdown', 'value'),
    State('idea-category-dropdown', 'value'),
    prevent_initial_call=True
)
def show_other_input_and_description(selected_value, selected_category):
    elements = []

    if selected_value == 'Others':
        elements.append(
            html.Div([
                dbc.Label("Please specify", className="fw-bold"),
                dcc.Textarea(
                    id='other-input',
                    placeholder='Reason for investment/expense...',
                    style={'width': '100%', 'height': '80px', 'fontSize': '14px'}
                )
            ])
        )

    if selected_value:
        elements.extend([
            html.Div([
                dbc.Label("Brief description of the work to be done", className="fw-bold"),
                dcc.Textarea(
                    id='description-input',
                    placeholder='Enter a short description of the proposed work...',
                    style={'width': '100%', 'height': '80px', 'fontSize': '14px'}
                )
            ]),
            html.Div([
                dbc.Label("Area of Impact", className="fw-bold"),
                dcc.Dropdown(
                    id='impact-dropdown' if selected_category == 'improvement' else 'impact-input',
                    options=(
                        [{'label': i, 'value': i} for i in ['Availability', 'TPOH', 'Utilization', 'Quality Rate']]
                        if selected_category == 'improvement' else None
                    ),
                    placeholder="Select area of impact" if selected_category == 'improvement' else 'Enter area of impact...',
                    style={'width': '100%'}
                ) if selected_category == 'improvement' else
                dcc.Input(
                    id='impact-input',
                    type='text',
                    placeholder='Enter area of impact...',
                    style={'width': '100%', 'height': '40px'}
                )
            ]),
            html.Div([
                dbc.Label("Scale of Impact", className="fw-bold"),
                dcc.Input(
                    id='scale-input',
                    type='text',
                    placeholder='Enter scale of impact...',
                    style={'width': '100%', 'height': '40px'}
                )
            ]),
            html.Div([
                dbc.Label("Investment Amount / Expenditure", className="fw-bold"),
                html.Div([
                    html.Span("₹", className="me-2", style={"fontSize": "20px"}),
                    dcc.Input(
                        id='amount-input',
                        type='text',
                        placeholder='Enter amount in INR...',
                        debounce=True,
                        style={'width': '60%', 'height': '40px'}
                    )
                ], className="d-flex align-items-center"),
                html.Div(id='amount-error', style={'color': 'red', 'fontSize': '12px', 'marginTop': '4px'})
            ]),
            html.Div([
                dbc.Label("Change Effective From:", className="fw-bold"),
                dmc.DatePickerInput(
                    id='effective-date',
                    placeholder='Select a date',
                    style={"width": "250px", "marginTop": "8px"}
                )
            ])
        ])

    return elements


def format_inr(value):
    x = str(value)
    last_three = x[-3:]
    rest = x[:-3]
    if rest != '':
        rest = re.sub(r'(\\d)(?=(\\d\\d)+$)', r'\\1,', rest)
        return rest + ',' + last_three
    else:
        return last_three


@app.callback(
    Output('amount-input', 'value'),
    Output('amount-error', 'children'),
    Input('amount-input', 'value'),
    prevent_initial_call=True
)
def validate_and_format_amount(val):
    if not val:
        return val, ""

    val_clean = val.replace(',', '').replace('₹', '').strip()

    if val_clean.replace('.', '', 1).isdigit():
        parts = val_clean.split('.')
        int_part = format_inr(parts[0])
        dec_part = f".{parts[1]}" if len(parts) > 1 else ''
        formatted = f"{int_part}{dec_part}"
        return formatted, ""
    else:
        return val, "Enter a valid amount"


if __name__ == '__main__':
    app.run(debug=True)
