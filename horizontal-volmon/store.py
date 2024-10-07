import panel as pn
import param

from panel_modal import Modal

pn.extension("modal", sizing_mode="stretch_width")
pn.extension(notifications=True)

class SignalMaker(param.Parameterized):
    option = param.ObjectSelector(default='Option 1', objects=['Option 1', 'Option 2', 'Option 3'])

    def __init__(self, state, **params):
        self.state = state

        # UI components
        self.signal_selector = pn.widgets.Select(name='Select', options=list(self.state.custom_signals.keys()))
        self.new_signal_button = pn.widgets.Button(name='New Signal', button_type='primary')

        # Form
        self.signal_name = pn.widgets.TextInput(name="Name", value="")

        self.value_formula = pn.widgets.TextInput(name="Value Formula", value="")
        self.value_colormap = pn.widgets.Select(name="Value Colormap", options=['viridis', 'plasma', 'inferno', 'magma'])
        self.value_lb = pn.widgets.FloatInput(name="Value Lower Bound", value=0)
        self.value_cb = pn.widgets.FloatInput(name="Value Center", value=50)
        self.value_ub = pn.widgets.FloatInput(name="Value Upper Bound", value=100)

        self.border_formula = pn.widgets.TextInput(name="Border Formula", value="")
        self.border_colormap = pn.widgets.Select(name="Border Colormap", options=['viridis', 'plasma', 'inferno', 'magma'])
        self.border_lb = pn.widgets.FloatInput(name="Border Lower Bound", value=0)
        self.border_cb = pn.widgets.FloatInput(name="Border Center", value=50)
        self.border_ub = pn.widgets.FloatInput(name="Border Upper Bound", value=100)

        self.bold_formula = pn.widgets.TextInput(name="Bold Formula", value="")

        # Save
        self.save_button = pn.widgets.Button(name="Save", button_type="primary")

        # Event handlers
        self.save_button.on_click(self.save_signal)

        # MYPANE
        self.mypane = pn.pane.JSON(self.state.custom_signals, name='XX')

        super().__init__(**params)

    # Save signal.
    def save_signal(self, event):

        if not self.signal_name.value or not self.value_formula.value:
            pn.state.notifications.error('This is an error notification.', duration=1000)
            return

        custom = True
        if self.signal_name.value in self.state.custom_signals:
            custom = self.state.custom_signals[self.signal_name.value]['custom']

        new_signal = {
            'value_formula': self.value_formula.value,
            'value_colormap': self.value_colormap.value,
            'value_lb': self.value_lb.value,
            'value_cb': self.value_cb.value,
            'value_ub': self.value_ub.value,
            'border_formula': self.border_formula.value,
            'border_colormap': self.border_colormap.value,
            'border_lb': self.border_lb.value,
            'border_cb': self.border_cb.value,
            'border_ub': self.border_ub.value,
            'bold_formula': self.bold_formula.value,
            'custom': custom
        }
        self.state.custom_signals[self.signal_name.value] = new_signal
        self.signal_selector.options = list(self.state.custom_signals.keys())
        self.signal_selector.value = self.signal_name.value
        
        self.state.dummy_depender = self.state.dummy_depender + 1

        # self.modal.is_open = True

    @pn.depends('signal_selector.value', watch=True)
    def load_signal(self):

        if not self.signal_selector.value:
            print("nothing")
            return

        if self.signal_selector.value in self.state.custom_signals:
            signal_data = self.state.custom_signals[self.signal_selector.value]
        else:
            signal_data = {
                'value_formula': '',
                'value_colormap': 'viridis',
                'value_lb': 0,
                'value_cb': 50,
                'value_ub': 100,
                'border_formula': '',
                'border_colormap': 'viridis',
                'border_lb': 0,
                'border_cb': 50,
                'border_ub': 100,
                'bold_formula': '',
                'custom': True
            }

        self.signal_name.value = self.signal_selector.value
        self.value_formula.value = signal_data['value_formula']
        self.value_colormap.value = signal_data['value_colormap']
        self.value_lb.value = signal_data['value_lb']
        self.value_cb.value = signal_data['value_cb']
        self.value_ub.value = signal_data['value_ub']
        self.border_formula.value = signal_data['border_formula']
        self.border_colormap.value = signal_data['border_colormap']
        self.border_lb.value = signal_data['border_lb']
        self.border_cb.value = signal_data['border_cb']
        self.border_ub.value = signal_data['border_ub']
        self.bold_formula.value = signal_data['bold_formula']

        if not signal_data['custom']:
            self.signal_name.disabled = True
            self.value_formula.disabled = True


    @param.depends('state.dummy_depender', watch=True)
    def refresh(self):
        print("WE ARE INSIDE HERE")
        print(self.state.custom_signals)
        self.mypane.object = self.state.custom_signals

    #@param.depends('state.dummy_depender')
    def view(self):
        print('hm')
        value_section = pn.Column(
            pn.pane.Markdown("### Value / Background Color"),
            self.value_formula,
            self.value_colormap,
            pn.Row(
                self.value_lb,
                self.value_cb,
                self.value_ub
            )
        )
        border_section = pn.Column(
            pn.pane.Markdown("### Border"),
            self.border_formula,
            self.border_colormap,
            pn.Row(
                self.border_lb,
                self.border_cb,
                self.border_ub
            )
        )
        bold_section = pn.Column(
            pn.pane.Markdown("### Bold"),
            self.bold_formula
        )
        self.modal = Modal(
            pn.Row(
                pn.Column(
                    self.signal_selector,
                    self.state.serialize_state,
                    self.mypane,
                    self.state.custom_signals,
                    width=400
                ),
                pn.Column(
                    pn.pane.Markdown("### Signal Name"),
                    self.signal_name,
                    value_section,
                    border_section,
                    bold_section,
                    self.save_button
                )
            )
        )
        return self.modal