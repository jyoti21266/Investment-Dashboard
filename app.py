import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_mantine_components as dmc
import re

app = dash.Dash(__name__, suppress_callback_exceptions=True, title="Investment Dashboard")

# Idea category options
idea_categories = [
    {'label': 'Improvement cum investment', 'value': 'improvement'},
    {'label': 'Infrastructure development', 'value': 'infrastructure'},
    {'label': 'Regulatory expenses', 'value': 'regulatory'},
    {'label': 'Fixed cost related idea', 'value': 'fixed_cost'},
]

# Reason options for non-improvement categories
category_to_changes = {
    'infrastructure': ['Construction of road', 'Painting related work', 'Creating shed', 'Installing sewage pipeline', 'Others'],
    'regulatory': ['New audit', 'Compliance training', 'Others'],
    'fixed_cost': ['Salary increase', 'Others']
}

# Layout
app.layout = dmc.MantineProvider(
    theme={"colorScheme": "dark"},
    children=html.Div([
        
    html.H2("Investment Dashboard", style={"textAlign": "center"}),

    html.Label("Investment/Expense Category", style={"fontWeight": "bold"}),
    dcc.Dropdown(
        id='idea-category-dropdown',
        options=idea_categories,
        placeholder="Select an Idea Category",
        style={'width': '60%'}
    ),

    html.Br(),
    html.Div(id='dynamic-container')
])
)

# Callback 1: Show second dropdown based on category
@app.callback(
    Output('dynamic-container', 'children'),
    Input('idea-category-dropdown', 'value')
)
def display_subcomponents(category):
    if not category:
        return None

    if category == 'improvement':
        lines = ['Pickling', '4-Hi Mill', 'ECL', 'BAF', 'SPM']
        return html.Div([
            html.Label("Select the Line", style={"fontWeight": "bold"}),
            dcc.Dropdown(
                id='line-dropdown',
                options=[{'label': line, 'value': line} for line in lines],
                placeholder="Select a process",
                style={'width': '60%'}
            ),
            html.Br(),
            html.Div(id='line-change-dropdown-container'),
            html.Div(id='other-input-container')
        ])
    else:
        return html.Div([
            html.Label("Reason for Investment/Expense", style={"fontWeight": "bold"}),
            dcc.Dropdown(
                id='change-dropdown',
                options=[{'label': item, 'value': item} for item in category_to_changes[category]],
                placeholder="Select change type",
                style={'width': '60%'}
            ),
            html.Br(),
            html.Div(id='other-input-container')
        ])

# Callback 2: Show reason dropdown under improvement
@app.callback(
    Output('line-change-dropdown-container', 'children'),
    Input('line-dropdown', 'value'),
    prevent_initial_call=True
)
def show_line_related_dropdown(selected_line):
    if selected_line and selected_line != 'Others':
        return html.Div([
            html.Label("Reason for investment/expense", style={"fontWeight": "bold"}),
            dcc.Dropdown(
                id='change-dropdown',
                options=[
                    {'label': 'Installation', 'value': 'Installation'},
                    {'label': 'Repair and Maintenance', 'value': 'Repair and Maintenance'},
                    {'label': 'Others', 'value': 'Others'}
                ],
                placeholder="Select change type",
                style={'width': '60%'}
            )
        ])
    return None

# Callback 3: All remaining inputs
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
                html.Label("Please specify", style={"fontWeight": "bold", "display": "block"}),
                dcc.Textarea(
                    id='other-input',
                    placeholder='Reason for investment/expense...',
                    style={
                        'width': '60%',
                        'height': '80px',
                        'marginTop': '8px',
                        'fontSize': '14px'
                    }
                )
            ])
        )

    if selected_value:
        # Description
        elements.append(
            html.Div([
                html.Label("Brief description of the work to be done", style={"fontWeight": "bold", "display": "block", "marginTop": "15px"}),
                dcc.Textarea(
                    id='description-input',
                    placeholder='Enter a short description of the proposed work...',
                    style={
                        'width': '60%',
                        'height': '80px',
                        'fontSize': '14px'
                    }
                )
            ])
        )

        # Area of Impact
        if selected_category == 'improvement':
            impact_options = ['Availability', 'TPOH', 'Utilization', 'Quality Rate']
            elements.append(
                html.Div([
                    html.Label("Area of Impact", style={"fontWeight": "bold", "display": "block", "marginTop": "15px"}),
                    dcc.Dropdown(
                        id='impact-dropdown',
                        options=[{'label': opt, 'value': opt} for opt in impact_options],
                        placeholder="Select area of impact",
                        style={'width': '60%'}
                    )
                ])
            )
        else:
            elements.append(
                html.Div([
                    html.Label("Area of Impact", style={"fontWeight": "bold", "display": "block", "marginTop": "15px"}),
                    dcc.Input(
                        id='impact-input',
                        type='text',
                        placeholder='Enter area of impact...',
                        style={
                            'width': '60%',
                            'height': '40px',
                            'fontSize': '14px',
                            'marginTop': '5px'
                        }
                    )
                ])
            )

        # Scale of Impact
        elements.append(
            html.Div([
                html.Label("Scale of Impact", style={"fontWeight": "bold", "display": "block", "marginTop": "15px"}),
                dcc.Input(
                    id='scale-input',
                    type='text',
                    placeholder='Enter scale of impact...',
                    style={
                        'width': '60%',
                        'height': '40px',
                        'fontSize': '14px',
                        'marginTop': '5px'
                    }
                )
            ])
        )

        # Investment Amount / Expenditure
        elements.append(
            html.Div([
                html.Label("Investment Amount / Expenditure", style={"fontWeight": "bold", "display": "block", "marginTop": "15px"}),
                html.Div([
                    html.Span("₹", style={"fontSize": "20px", "marginRight": "5px"}),
                    dcc.Input(
                        id='amount-input',
                        type='text',
                        placeholder='Enter amount in INR...',
                        debounce=True,
                        style={
                            'width': '40%',
                            'height': '40px',
                            'fontSize': '14px',
                            'marginTop': '5px'
                        }
                    )
                ], style={'display': 'flex', 'alignItems': 'center'}),
                html.Div(id='amount-error', style={'color': 'red', 'fontSize': '12px', 'marginTop': '4px'})
            ])
        )

        # Month-Year Dropdowns
        elements.append(
    html.Div([
        html.Label("Change Effective From:", style={"fontWeight": "bold", "display": "block", "marginTop": "15px"}),
        dmc.DatePickerInput(
            id='effective-date',
            placeholder='Select a date',
            style={"width": "250px", "marginTop": "8px"}
        )
    ])
)

    return elements

# Helper for Indian number formatting
def format_inr(value):
    x = str(value)
    last_three = x[-3:]
    rest = x[:-3]
    if rest != '':
        rest = re.sub(r'(\d)(?=(\d\d)+$)', r'\1,', rest)
        return rest + ',' + last_three
    else:
        return last_three

# Callback to validate and format INR field
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

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

