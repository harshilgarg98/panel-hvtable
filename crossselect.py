import panel as pn
import param

class CustomCrossSelectApp(param.Parameterized):
    available_items = param.List(['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry', 'Fig', 'Grape'])
    selected_items = param.List([])
    filter_text = param.String(default="")

    def __init__(self, **params):
        super().__init__(**params)
        self.filter_input = pn.widgets.TextInput(name="Filter", placeholder="Enter filter text", value_input="")
        self.available_select = pn.widgets.MultiSelect(
            name='Available Items',
            options=self.available_items,
            size=6
        )
        self.selected_select = pn.widgets.MultiSelect(
            name='Selected Items',
            options=self.selected_items,
            size=6
        )
        self.add_button = pn.widgets.Button(name='>>', button_type='default')
        self.remove_button = pn.widgets.Button(name='<<', button_type='default')
        self.up_button = pn.widgets.Button(name='Move Up', button_type='default')
        self.down_button = pn.widgets.Button(name='Move Down', button_type='default')
        self.add_button.on_click(self.add_items)
        self.remove_button.on_click(self.remove_items)
        self.up_button.on_click(self.move_up)
        self.down_button.on_click(self.move_down)
        self.available_select.on_double_click(self.add_items)
        self.selected_select.on_double_click(self.remove_items)

        self.filter_input.param.watch(self.filter_available_items, 'value_input')

    @param.depends('available_items', 'selected_items', 'filter_text', watch=True)
    def _update_selects(self):
        filtered_items = [item for item in self.available_items if self.filter_text.lower() in item.lower()]
        self.available_select.options = filtered_items
        self.selected_select.options = self.selected_items

    def filter_available_items(self, event):
        self.filter_text = event.new
        self.param.trigger('filter_text')

    def add_items(self, event):
        items_to_add = list(self.available_select.value)
        for item in items_to_add:
            if item not in self.selected_items:
                t = list(self.selected_items)
                t.append(item)
                self.selected_items = t
        self.available_items = [item for item in self.available_items if item not in self.selected_items]
        self.param.trigger('available_items')
        self.param.trigger('selected_items')

    def remove_items(self, event):
        items_to_remove = list(self.selected_select.value)
        self.selected_items = [item for item in self.selected_items if item not in items_to_remove]
        for item in items_to_remove:
            if item not in self.available_items:
                t = list(self.available_items)
                t.append(item)
                self.available_items = t
        self.param.trigger('available_items')
        self.param.trigger('selected_items')

    def move_up(self, event):
        selected = list(self.selected_select.value)
        if selected:
            new_order = self.selected_items.copy()
            for item in selected:
                idx = new_order.index(item)
                if idx > 0:
                    new_order[idx-1], new_order[idx] = new_order[idx], new_order[idx-1]
            self.selected_items = new_order
            self.param.trigger('selected_items')

    def move_down(self, event):
        selected = list(self.selected_select.value)
        if selected:
            new_order = self.selected_items.copy()
            for item in reversed(selected):
                idx = new_order.index(item)
                if idx < len(new_order) - 1:
                    new_order[idx], new_order[idx+1] = new_order[idx+1], new_order[idx]
            self.selected_items = new_order
            self.param.trigger('selected_items')

    def view(self):
        left_column = pn.Column(
            pn.pane.Markdown("### Available Items"),
            pn.Spacer(height=0),
            self.filter_input,
            self.available_select
        )

        center_column = pn.Column(
            pn.Spacer(height=120),  # Adjust this value to align buttons vertically
            self.add_button,
            pn.Spacer(height=0),
            self.remove_button,
            align=('center', 'center')
        )

        right_column = pn.Column(
            pn.pane.Markdown("### Selected Items"),
            pn.Spacer(height=17),
            pn.Row(self.up_button,self.down_button),
            self.selected_select
        )

        return pn.Row(
            left_column,
            center_column,
            right_column,
            align='start'
        )

app = CustomCrossSelectApp()
pn.extension()
app.view().servable()