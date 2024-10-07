import param as pm
import panel as pn

from panel_modal import Modal

pn.extension("modal", sizing_mode="stretch_width")

class SignalSelector(pm.Parameterized):
    def __init__(self, state, **params):
        self.state = state

        # UI components
        self.filter_input = pn.widgets.TextInput(name="Filter", placeholder="Enter filter text", value_input="")
        self.available_signals_selector = pn.widgets.MultiSelect(
            name='Available Columns',
            options=self.state.available_signals,
            size=12
        )
        self.selected_signals_selector = pn.widgets.MultiSelect(
            name='Selected Columns',
            options=self.state.selected_signals,
            size=12
        )
        self.add_button = pn.widgets.Button(name='Add', button_type='default')
        self.remove_button = pn.widgets.Button(name='Remove', button_type='default')
        self.up_button = pn.widgets.Button(name='Up', button_type='default')
        self.down_button = pn.widgets.Button(name='Down', button_type='default')

        # Event handlers
        self.add_button.on_click(self.add_items)
        self.remove_button.on_click(self.remove_items)
        self.up_button.on_click(self.move_up)
        self.down_button.on_click(self.move_down)
        self.available_signals_selector.on_double_click(self.add_items)
        self.selected_signals_selector.on_double_click(self.remove_items)
        
        # Super constructor
        super().__init__(**params)

    @pm.depends('state.available_signals', 'state.selected_signals', 'filter_input.value_input', watch=True)
    def refresh(self):
        self.available_signals_selector.options = [item for item in self.state.available_signals if self.filter_input.value_input.lower() in item.lower()]
        self.selected_signals_selector.options = self.state.selected_signals

    @pm.depends('state.custom_signals', watch=True)
    def reload_signals(self):
        t, u, v = list(self.state.available_signals), list(self.state.selected_signals), list(self.state.custom_signals.keys())

        # Looks for newly deleted signals
        t = [x for x in t if x in v]
        u = [x for x in u if x in v]

        # Poon!
        for signal in list(self.state.custom_signals.keys()):
            # Look for newly added signals
            if signal not in t and signal not in u:
                t.append(signal)
        self.state.param.update(
            available_signals=t,
            selected_signals=u
        )


    def add_items(self, event):
        a = list(self.state.selected_signals) + list(self.available_signals_selector.value)
        b = [item for item in self.state.available_signals if item not in a]
        self.state.param.update(
            available_signals=b,
            selected_signals=a
        )

    def remove_items(self, event):
        selected = list(self.selected_signals_selector.value)
        a = list(self.state.available_signals) + selected
        b = [item for item in self.state.selected_signals if item not in selected]
        self.state.param.update(
            available_signals=a,
            selected_signals=b
        )
        
    def move_up(self, event):
        selected = list(self.selected_signals_selector.value)
        sorted_order = self.state.selected_signals.copy()
        if selected:
            new_order = sorted_order.copy()
            for item in selected:
                idx = new_order.index(item)
                if idx > 0:
                    new_order[idx-1], new_order[idx] = new_order[idx], new_order[idx-1]
            sorted_order = new_order
        self.state.selected_signals = sorted_order

    def move_down(self, event):
        selected = list(self.selected_signals_selector.value)
        sorted_order = self.state.selected_signals.copy()
        if selected:
            new_order = sorted_order.copy()
            for item in reversed(selected):
                idx = new_order.index(item)
                if idx < len(new_order) - 1:
                    new_order[idx], new_order[idx+1] = new_order[idx+1], new_order[idx]
            sorted_order = new_order
        self.state.selected_signals = sorted_order

    def view(self):
        left_column = pn.Column(
            pn.pane.Markdown("### Available Columns"),
            self.filter_input,
            self.available_signals_selector,
            width=400
        )
        center_column = pn.Column(
            pn.Spacer(height=120),
            self.add_button,
            self.remove_button,
            align=('center', 'center'),
            width=100
        )
        right_column = pn.Column(
            pn.pane.Markdown("### Selected Columns"),
            pn.Spacer(height=17),
            pn.Row(self.up_button,self.down_button, width=100),
            self.selected_signals_selector,
            width=400
        )
        self.modal = Modal(
            pn.Column(
                "## Signal Selector",
                pn.Row(
                    left_column,
                    center_column,
                    right_column,
                    align='start'
                )
            )
        )
        return self.modal