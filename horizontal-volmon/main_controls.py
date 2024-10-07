import param
import panel as pn

class MainControls(param.Parameterized):

    def __init__(self, state, **params):
        self.state = state

        # UI components
        self.expiration_selector = pn.widgets.Select(
            name='Expiration',
            options=self.state.available_expirations,
            value=self.state.selected_expiration,
            width=150
        )
        self.group_checkbox = pn.widgets.Checkbox(name='Group by Sector', value=self.state.grouped)
        self.custom_filter = pn.widgets.TextInput(name='Custom Filter', value=self.state.custom_filter, width=300)
        self.update_button = pn.widgets.Button(name='Update', button_type='primary', width=100)
        self.clear_button = pn.widgets.Button(name='Clear', button_type='default', width=100)
        self.refresh_button = pn.widgets.Button(name="Generate New Data", button_type="primary")

        self.update_button.on_click(self.update_custom_filter)
        self.clear_button.on_click(self.clear_custom_filter)

        # Super constructor
        super().__init__(**params)


    @pn.depends(
        'expiration_selector.value',
        'group_checkbox.value',
        watch=True
    )
    def update_state(self):
        self.state.selected_expiration = self.expiration_selector.value
        self.state.grouped = self.group_checkbox.value

        print(self.state.serialize_state())

    def update_custom_filter(self, event):
        self.state.custom_filter = self.custom_filter.value
    
    def clear_custom_filter(self, event):
        self.custom_filter.value = ''
        self.state.custom_filter = ''

    def view(self):
        return pn.Column(
            pn.Row(self.expiration_selector, pn.Column(pn.Spacer(height=24), self.group_checkbox), self.refresh_button),
            pn.Row(pn.Column(self.custom_filter, width=320), pn.Column(pn.Spacer(height=16), self.update_button, width=120), pn.Column(pn.Spacer(height=16), self.clear_button), width=200),
        )
