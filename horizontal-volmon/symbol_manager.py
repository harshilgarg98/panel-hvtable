import param
import panel as pn

from panel_modal import Modal

pn.extension("modal", sizing_mode="stretch_width")

class SymbolManager(param.Parameterized):

    def __init__(self, state, **params):
        self.state = state

        # UI components
        self.trader_selector = pn.widgets.MultiChoice(
            name='Trader Bucket Label',
            options=self.state.available_trader_buckets,
            value=[],
            width=600
        )
        self.sector_selector = pn.widgets.MultiChoice(
            name='Sector',
            options=self.state.available_sectors,
            value=[],
            width=600
        )
        self.additional_symbols_selector = pn.widgets.TextInput(name='Additional Symbols', width=600)
        self.excluded_symbols_selector = pn.widgets.TextInput(name='Excluded Symbols', width=600)

        # Super constructor
        super().__init__(**params)

    @pn.depends(
        'trader_selector.value',
        'sector_selector.value',
        'additional_symbols_selector.value_input',
        'excluded_symbols_selector.value_input', 
        watch=True
    )
    def update_state(self):
        self.state.selected_trader_buckets = self.trader_selector.value
        self.state.selected_sectors = self.sector_selector.value
        self.state.additional_symbols = self.additional_symbols_selector.value_input
        self.state.excluded_symbols = self.excluded_symbols_selector.value_input

        print(self.state.serialize_state())

    def view(self):
        self.modal = Modal(
            pn.Column(
                "## Symbol Selector",
                self.trader_selector,
                self.sector_selector,
                self.additional_symbols_selector,
                self.excluded_symbols_selector
            )
        )
        return self.modal