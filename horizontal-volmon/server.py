import panel as pn

import param
from panel_modal import Modal

pn.extension()
pn.extension('tabulator')
pn.extension("modal", sizing_mode="stretch_width")
pn.extension(notifications=True)

from application_state import ApplicationState
from symbol_manager import SymbolManager
from signal_selector import SignalSelector
from main_controls import MainControls
from signal_maker import SignalMaker

#########################################################################################################
import pandas as pd
import numpy as np
import random
import string
import filter_utils

trader_buckets = ['GARGH', 'FLETCHERMI', 'WANGCLA', 'CHENRYA', 'LIALV', 'JIANGJ']
expirations = ['2024-09-06', '2024-09-13', '2024-09-20', '2024-09-27', 
                    '2024-10-04', '2024-10-11', '2024-10-18', '2024-11-15', '2024-12-20']
sectors = ['Semiconductors', 'Industrials', 'Travel', 'Software I', 'Software II', 'Materials', 
           'Real Estate', 'Pharmaceuticals', 'Healthcare Services', 'Financial Services', 
           'Consumer Discretionary', 'Communication Services', 'Consumer Staples', 'Utilities']

# Function to create dummy dataframe
n_rows = 100
data = {
    "Sector": np.random.choice(sectors, n_rows),
    "Symbol": [''.join(random.choices(string.ascii_uppercase, k=3)) for _ in range(n_rows)],
    "FairPrice": np.random.uniform(10, 500, n_rows).round(2),
    "SpotReturn": np.random.uniform(-10, 10, n_rows).round(2),
    "TermTotalVol": np.random.uniform(20, 100, n_rows).round(2),
    "Expiration": np.random.choice(expirations, n_rows),
    "TraderBucketLabel": np.random.choice(trader_buckets, n_rows)
}

df = pd.DataFrame(data)
df["Spot1N"] = (df["SpotReturn"] / (df["TermTotalVol"] / 20)).round(4)
df["BillonSignal1"] = np.random.uniform(-5, 5, n_rows).round(2)
df["BillonSignal2"] = np.random.uniform(-5, 5, n_rows).round(2)
df["BillonSignal3"] = np.random.uniform(-5, 5, n_rows).round(2)

all_columns = df.columns.tolist()
frozen_columns = ['Symbol']
selectable_columns = [col for col in all_columns if col not in frozen_columns]
necessary_columns = ['Sector']

available_expirations = ['All'] + sorted(df['Expiration'].unique().tolist())
selected_expiration = 'All'

#########################################################################################################

def make_default_signals():
    t = dict()
    for column in selectable_columns:
        t[column] = {
            'value_formula': column,
            'value_colormap': 'None',
            'value_lb': -1,
            'value_cb': 0,
            'value_ub': 1,
            'border_formula': '',
            'border_colormap': 'None',
            'border_lb': -1,
            'border_cb': 0,
            'border_ub': 1,
            'bold_formula': '',
            'custom': False
        }
    return t

state = ApplicationState(
    available_trader_buckets=trader_buckets,
    available_sectors=sectors,
    available_signals=[],
    selected_signals=selectable_columns,
    available_expirations=available_expirations,
    selected_expiration=selected_expiration,
    custom_signals=make_default_signals()
)
symbol_manager = SymbolManager(state=state)
signal_selector = SignalSelector(state=state)
signal_maker = SignalMaker(state=state)
main_controls = MainControls(state=state)

#########################################################################################################

def build_custom_column(ds, custom_signals):
    ds = ds.copy()
    for signal_name in list(custom_signals.keys()):
        signal = custom_signals[signal_name]
        if signal['custom']:
            print("Custom Signal:", signal)
            t = ds.eval(signal['value_formula'], engine="numexpr")
            ds[signal_name] = t
    return ds


@pn.depends(state.param.selected_expiration)
def expiration_header(selected_expiration):
    return pn.pane.Markdown(f"## Selected Expiration: {selected_expiration}")

@pn.depends(
    state.param.selected_trader_buckets,
    state.param.selected_sectors,
    state.param.additional_symbols,
    state.param.excluded_symbols,
    state.param.custom_filter,
    state.param.selected_expiration,
    state.param.selected_signals,
    state.param.grouped,
    state.param.custom_signals
)
def render_table(
    selected_trader_buckets, selected_sectors, additional_symbols, excluded_symbols, custom_filter,selected_expiration, selected_signals, grouped, custom_signals):
    
    filtered_df = df.copy()

    # Symbol selector
    if not selected_trader_buckets and not selected_sectors and not additional_symbols:
        include_symbol_mask = np.full(len(filtered_df), True, dtype='bool')
    else:
        include_symbol_mask = (
            filtered_df.TraderBucketLabel.isin(selected_trader_buckets) |
            filtered_df.Sector.isin(selected_sectors) |
            filtered_df.Symbol.isin(additional_symbols.split(","))
        )
    exclude_symbol_mask = (
        filtered_df.Symbol.isin(excluded_symbols.split(","))
    )
    filtered_df = filtered_df[include_symbol_mask & ~exclude_symbol_mask]

    # Add custom signal columns
    filtered_df = build_custom_column(filtered_df, custom_signals)

    # Expiration selector
    if selected_expiration != 'All':
        filtered_df = filtered_df[filtered_df['Expiration'] == selected_expiration]

    # Custom filter
    filtered_df = filter_utils.smart_filter(filtered_df, custom_filter)

    # Column selector
    column_order = frozen_columns + selected_signals
    hidden_columns = []
    for necessary_column in necessary_columns:
        if necessary_column not in column_order:
            column_order.append(necessary_column)
            hidden_columns.append(necessary_column)
    filtered_df = filtered_df[column_order]

    # Grouped
    grouping = ['Sector'] if grouped else []

    # Table
    tabulator = pn.widgets.Tabulator(
        filtered_df, 
        pagination='remote', 
        page_size=15, 
        sizing_mode='stretch_width', 
        frozen_columns=frozen_columns,
        hidden_columns=hidden_columns,
        groupby=grouping,
        show_index=False
    )
    return pn.Column(tabulator)

def setup_menu():
    def handle_menu(event):
        if event.obj.clicked == 'Symbol Manager':
            symbol_manager.modal.is_open = True
        elif event.obj.clicked == 'Signal Selector':
            signal_selector.modal.is_open = True
        elif event.obj.clicked == 'Signal Maker':
            signal_maker.modal.is_open = True
    menu_items = [('Symbol Manager', 'Symbol Manager'), ('Signal Selector', 'Signal Selector'), ('Signal Maker', 'Signal Maker'), None, ('Import', 'Import'), ('Save', 'Save')]
    menu_button = pn.widgets.MenuButton(name='Settings', items=menu_items, button_type='primary', width=200)
    menu_button.on_click(handle_menu)
    return menu_button

layout = pn.Column(
    pn.Row(pn.pane.Markdown("# Horizontal Voltable"), setup_menu()),
    symbol_manager.view,
    signal_selector.view,
    main_controls.view,
    signal_maker.view,
    expiration_header,
    render_table
)
layout.servable()