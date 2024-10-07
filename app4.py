import asyncio
import panel as pn
import pandas as pd
import numpy as np
import random
import string
import filter_utils
import param
from panel_modal import Modal
import time

# Enable Panel extension for Jupyter Notebook
pn.extension('tabulator')
pn.extension("modal", sizing_mode="stretch_width")

from volmon.basil_manager import status

# Global constants
TRADER_BUCKETS = ['GARGH', 'FLETCHERMI', 'WANGCLA', 'CHENRYA', 'LIALV', 'JIANGJ']
EXPIRATION_DATES = ['2024-09-06', '2024-09-13', '2024-09-20', '2024-09-27', 
                    '2024-10-04', '2024-10-11', '2024-10-18', '2024-11-15', '2024-12-20']
SECTORS = ['Semiconductors', 'Industrials', 'Travel', 'Software I', 'Software II', 'Materials', 
           'Real Estate', 'Pharmaceuticals', 'Healthcare Services', 'Financial Services', 
           'Consumer Discretionary', 'Communication Services', 'Consumer Staples', 'Utilities']

# Function to generate random 3-character string
def random_symbol():
    return ''.join(random.choices(string.ascii_uppercase, k=3))

# Function to create dummy dataframe
@pn.cache
def create_dummy_dataframe(n_rows=100):
    data = {
        "Sector": np.random.choice(SECTORS, n_rows),
        "Symbol": [random_symbol() for _ in range(n_rows)],
        "FairPrice": np.random.uniform(10, 500, n_rows).round(2),
        "SpotReturn": np.random.uniform(-10, 10, n_rows).round(2),
        "TermTotalVol": np.random.uniform(20, 100, n_rows).round(2),
        "Expiration": np.random.choice(EXPIRATION_DATES, n_rows),
        "TraderBucketLabel": np.random.choice(TRADER_BUCKETS, n_rows)
    }
    
    df = pd.DataFrame(data)
    df["Spot1N"] = (df["SpotReturn"] / (df["TermTotalVol"] / 20)).round(4)
    df["BillonSignal"] = np.random.uniform(-5, 5, n_rows).round(2)
    
    return df

# Create initial dataframe
df = create_dummy_dataframe()

# Define all columns, fixed columns, and selectable columns
ALL_COLUMNS = pn.state.cache['df'].columns.tolist()
FIXED_COLUMNS = ['Symbol']
SELECTABLE_COLUMNS = [col for col in ALL_COLUMNS if col not in FIXED_COLUMNS]

from volmon import custom_cross_selector, custom_symbol_selector

# Create the CustomCrossSelectApp instance
symbol_selector =  custom_symbol_selector.SymbolSelector(trader_buckets=TRADER_BUCKETS, sectors=SECTORS)
column_selector = custom_cross_selector.CrossSelector(available_items=[], selected_items=SELECTABLE_COLUMNS)

# Create a Tabulator widget
tabulator = pn.widgets.Tabulator(
    df, 
    pagination='remote', 
    page_size=15, 
    sizing_mode='stretch_width', 
    frozen_columns=['Symbol'],
    show_index=False
)

# Create a select input for Expiration
expiration_selector = pn.widgets.Select(
    name='Expiration',
    options=['All'] + sorted(df['Expiration'].unique().tolist()),
    value='All',  # Start with 'All' selected
    width=150
)


# Create a checkbox for grouping
group_checkbox = pn.widgets.Checkbox(name='Group by Sector', value=False)

# Create a text input for custom filter
custom_filter = pn.widgets.TextInput(name='Custom Filter', value='', width=300)

# Create buttons for update and clear
update_button = pn.widgets.Button(name='Update', button_type='primary', width=100)
clear_button = pn.widgets.Button(name='Clear', button_type='default', width=100)

# Function to update table columns
@pn.depends(column_selector.param.selected_items, watch=True)
def update_table_columns(selected_items):
    
    # Combine fixed columns with selected columns
    display_columns = FIXED_COLUMNS + selected_items
    
    # Ensure 'Sector' is in the dataframe even if not selected
    if 'Sector' not in display_columns:
        display_columns.append('Sector')
    
    # Update the dataframe with fixed columns, selected columns, and 'Sector'
    filtered_df = df[display_columns]
    
    # Update the Tabulator widget
    tabulator.value = filtered_df
    
    # Update visible columns (excluding 'Sector' if not selected)
    visible_columns = [col for col in display_columns if col != 'Sector' or 'Sector' in selected_items]
    tabulator.columns = [{'field': col} for col in visible_columns]
    
    # Update hidden columns
    hidden_columns = [col for col in display_columns if col not in visible_columns]
    tabulator.hidden_columns = hidden_columns
    
    # Ensure Symbol is always frozen
    tabulator.frozen_columns = ['Symbol']

    filter_dataframe(None)

# Define the filter function
def filter_dataframe(event):
    global df
    filtered_df = df.copy()
    
    # # Apply TraderBucketLabel filter
    # if trader_selector.value:
    #     filtered_df = filtered_df[filtered_df['TraderBucketLabel'].isin(trader_selector.value)]

    # if sector_selector.value:
    #     filtered_df = filtered_df[filtered_df['Sector'].isin(sector_selector.value)]

    #     # Apply additional symbols filter
    # if additional_symbols.value_input:
    #     add_symbols = [s.strip() for s in additional_symbols.value_input.split(',')]
    #     additional_rows = df[df['Symbol'].isin(add_symbols)]
    #     filtered_df = pd.concat([filtered_df, additional_rows]).drop_duplicates()
    
    # # Apply excluded symbols filter
    # if excluded_symbols.value_input:
    #     excl_symbols = [s.strip() for s in excluded_symbols.value_input.split(',')]
    #     filtered_df = filtered_df[~filtered_df['Symbol'].isin(excl_symbols)]

    filtered_df = symbol_selector.filter_symbols(filtered_df)
    
    # Apply Expiration filter
    if expiration_selector.value != 'All':
        filtered_df = filtered_df[filtered_df['Expiration'] == expiration_selector.value]

    print(len(filtered_df))
    
    # Apply custom filter if the update button was pressed
    if event and event.obj == update_button:
        print(f"Custom filter value: {custom_filter.value}")
        filtered_df = filter_utils.smart_filter(filtered_df, custom_filter.value)
        print(len(filtered_df))
    
    # Apply grouping if checkbox is checked
    if group_checkbox.value:
        tabulator.groupby = ['Sector']
    else:
        tabulator.groupby = []
    
    # Combine fixed columns with selected columns and ensure 'Sector' is included
    display_columns = FIXED_COLUMNS + column_selector.selected_items
    if 'Sector' not in display_columns:
        display_columns.append('Sector')
    
    filtered_df = filtered_df[display_columns]
    
    tabulator.value = filtered_df
    
    # Update visible columns (excluding 'Sector' if not selected)
    visible_columns = [col for col in display_columns if col != 'Sector' or 'Sector' in column_selector.selected_items]
    tabulator.columns = [{'field': col} for col in visible_columns]
    
    # Update hidden columns
    hidden_columns = [col for col in display_columns if col not in visible_columns]
    tabulator.hidden_columns = hidden_columns

# async def update_data():
#     global df
#     df = create_dummy_dataframe()  # This will now use the cached version
#     expiration_selector.options = ['All'] + sorted(df['Expiration'].unique().tolist())
#     filter_dataframe(None)  # Reapply filters to the new data

# pn.state.schedule_task('update_data', update_data, period=5000)

# Attach the filter function to the selectors, checkbox, and update button
symbol_selector.trader_selector.param.watch(filter_dataframe, 'value')
symbol_selector.sector_selector.param.watch(filter_dataframe, 'value')
expiration_selector.param.watch(filter_dataframe, 'value')
symbol_selector.additional_symbols.param.watch(filter_dataframe, 'value_input')
symbol_selector.excluded_symbols.param.watch(filter_dataframe, 'value_input')
group_checkbox.param.watch(filter_dataframe, 'value')
update_button.on_click(filter_dataframe)

# Define the clear function
def clear_custom_filter(event):
    custom_filter.value = ''
    filter_dataframe(event)

# Attach the clear function to the clear button
clear_button.on_click(clear_custom_filter)

# Create a button to refresh the data
refresh_button = pn.widgets.Button(name="Generate New Data", button_type="primary")

# Define the refresh function
def refresh_data(event=None):
    global df
    new_df = create_dummy_dataframe()
    expiration_selector.options = ['All'] + sorted(new_df['Expiration'].unique().tolist())
    return new_df

# def periodic_update():
#     global df
#     new_df = refresh_data()
#     df = new_df
#     filter_dataframe(None)  # Apply current filters to the new data

# pn.state.add_periodic_callback(periodic_update, period=5000)  # 5000 milliseconds = 5 seconds

# Attach the refresh function to the button
refresh_button.on_click(refresh_data)

# Create a header to display the selected expiration
expiration_header = pn.pane.Markdown("## Selected Expiration: All")

def update_expiration_header(event):
    expiration_header.object = f"## Selected Expiration: {expiration_selector.value}"

expiration_selector.param.watch(update_expiration_header, 'value')

# Ensure update_table_columns is called when the app is initialized
update_table_columns(column_selector.selected_items)

signal_modal_content = column_selector.view()
signal_modal = Modal(signal_modal_content)


symbol_modal_content = symbol_selector.view()
symbol_modal = Modal(symbol_modal_content)


# Menu
def handle_menu(event):
    print(event)
    if event.obj.clicked == 'Symbols':
        symbol_modal.is_open = True
    elif event.obj.clicked == 'Signals':
        signal_modal.is_open = True

menu_items = [('Symbols', 'Symbols'), ('Signals', 'Signals'), None, ('Import', 'Import'), ('Save', 'Save')]
menu_button = pn.widgets.MenuButton(name='Settings', items=menu_items, button_type='primary', width=100)
menu_button.on_click(handle_menu)

# Create the app layout
app = pn.Column(
    pn.Row(pn.pane.Markdown("# Horizontal Voltable"), menu_button),
    pn.Row(expiration_selector, pn.Column(pn.Spacer(height=24), group_checkbox), refresh_button),
    pn.Row(pn.Column(custom_filter, width=320), pn.Column(pn.Spacer(height=16), update_button, width=120), pn.Column(pn.Spacer(height=16), clear_button), width=200),
    pn.Row(symbol_modal),
    pn.Row(signal_modal),
    expiration_header,
    tabulator
)

# Display the app
app.servable()


# Expiration header
# Convert to modals
# Handle menu button