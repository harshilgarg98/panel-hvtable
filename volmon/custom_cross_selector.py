import param as pm
import panel as pn

class CrossSelector(pm.Parameterized):
    available_items = pm.List([])
    selected_items = pm.List([])

    def __init__(self, **params):
        super().__init__(**params)

        # UI components
        self.filter_input = pn.widgets.TextInput(name="Filter", placeholder="Enter filter text", value_input="")
        self.available_select = pn.widgets.MultiSelect(
            name='Available Columns',
            options=self.available_items,
            size=12
        )
        self.selected_select = pn.widgets.MultiSelect(
            name='Selected Columns',
            options=self.selected_items,
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
        self.available_select.on_double_click(self.add_items)
        self.selected_select.on_double_click(self.remove_items)
        
        pn.bind(
            self.refresh,
            available_items=self.param.available_items,
            selected_items=self.param.selected_items,
            filter_text=self.filter_input.param.value_input,
            watch=True
        )

    def refresh(self, available_items, selected_items, filter_text):
        self.available_select.options = [item for item in available_items if filter_text.lower() in item.lower()]
        self.selected_select.options = selected_items

    def add_items(self, event):
        self.selected_items = list(self.selected_items) + list(self.available_select.value)
        self.available_items = [item for item in self.available_items if item not in self.selected_items]

    def remove_items(self, event):
        self.available_items = list(self.available_items) + list(self.selected_select.value)
        self.selected_items = [item for item in self.selected_items if item not in self.available_items]
        
    def move_up(self, event):
        selected = list(self.selected_select.value)
        if selected:
            new_order = self.selected_items.copy()
            for item in selected:
                idx = new_order.index(item)
                if idx > 0:
                    new_order[idx-1], new_order[idx] = new_order[idx], new_order[idx-1]
            self.selected_items = new_order

    def move_down(self, event):
        selected = list(self.selected_select.value)
        if selected:
            new_order = self.selected_items.copy()
            for item in reversed(selected):
                idx = new_order.index(item)
                if idx < len(new_order) - 1:
                    new_order[idx], new_order[idx+1] = new_order[idx+1], new_order[idx]
            self.selected_items = new_order

    def view(self):
        left_column = pn.Column(
            pn.pane.Markdown("### Available Columns"),
            self.filter_input,
            self.available_select,
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
            self.selected_select,
            width=400
        )

        return pn.Column(
            "## Signal Selector",
            pn.Row(
                left_column,
                center_column,
                right_column,
                align='start'
            ),
            sizing_mode="stretch_width",
            width=1000
        )