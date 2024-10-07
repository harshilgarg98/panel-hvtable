import panel as pn
import colorcet as cc
import param

from panel_modal import Modal

pn.extension("modal", sizing_mode="stretch_width")
pn.extension(notifications=True)

css = """
.widget-box {
  overflow: scroll;
}
"""

pn.extension(raw_css=[css])

class SignalMaker(param.Parameterized):

    def __init__(self, state, **params):
        self.state = state

        # UI components
        self.signal_selector = pn.widgets.AutocompleteInput(name='Select', options=list(self.state.custom_signals.keys()), case_sensitive=False, min_characters=0, search_strategy='includes')
        self.new_signal_button = pn.widgets.Button(name='New Signal', button_type='primary')

        # Form
        self.signal_name = pn.widgets.TextInput(name="Name", value="")

        self.value_formula = pn.widgets.TextInput(name="Value Formula", value="")
        self.value_colormap = pn.widgets.ColorMap(name="Value Colormap", options=cc.palette, swatch_width=50)
        self.value_lb = pn.widgets.FloatInput(name="Value Lower Bound", value=0)
        self.value_cb = pn.widgets.FloatInput(name="Value Center", value=50)
        self.value_ub = pn.widgets.FloatInput(name="Value Upper Bound", value=100)

        self.border_formula = pn.widgets.TextInput(name="Border Formula", value="")
        self.border_colormap = pn.widgets.Select(name="Border Colormap", options=['None', 'viridis', 'plasma', 'inferno', 'magma'])
        self.border_lb = pn.widgets.FloatInput(name="Border Lower Bound", value=0)
        self.border_cb = pn.widgets.FloatInput(name="Border Center", value=50)
        self.border_ub = pn.widgets.FloatInput(name="Border Upper Bound", value=100)

        self.bold_formula = pn.widgets.TextInput(name="Bold Formula", value="")

        # Save
        self.new_signal_button = pn.widgets.Button(name="New Signal", button_type="primary")
        self.save_button = pn.widgets.Button(name="Save", button_type="primary")
        self.delete_button = pn.widgets.Button(name="Delete", button_type="danger")

        # Event handlers
        self.new_signal_button.on_click(self.make_new_signal)
        self.save_button.on_click(self.save_signal)
        self.delete_button.on_click(self.delete_signal)

        # MYPANE
        if self.signal_selector.value:
            self.mypane = pn.pane.JSON(self.state.custom_signals[self.signal_selector.value], name='XX')
        else:
            self.mypane = pn.pane.JSON({}, name='XX')

        self.signal_selector.value = self.signal_selector.options[0]
        self.load_signal()
        self.refresh()
        #self.signal_selector.value = 'Sector'

        super().__init__(**params)

    def make_new_signal(self, event):
        if 'New Signal' in self.signal_selector.options:
            pn.state.notifications.error('This is an error notification.', duration=1000)
            return
        self.signal_selector.options = list(self.signal_selector.options) + ['New Signal']
        self.signal_selector.value = 'New Signal'

    # Save signal.
    def save_signal(self, event):

        if not self.signal_name.value or self.signal_name.value == 'New Signal' or not self.value_formula.value:
            pn.state.notifications.error('This is an error notification.', duration=1000)
            return

        name = self.signal_name.value

        custom = True
        if self.signal_name.value in self.state.custom_signals:
            custom = self.state.custom_signals[self.signal_name.value]['custom']

        new_signal = {
            'value_formula': self.value_formula.value,
            'value_colormap': self.value_colormap.value_name,
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
        currdict = dict(self.state.custom_signals)
        currdict[name] = new_signal
        self.state.custom_signals = currdict
        
        self.signal_selector.options = list(self.state.custom_signals.keys())
        self.signal_selector.value = name

    def delete_signal(self, event):
        t = self.signal_selector.value
        if t not in self.state.custom_signals:
            if t == 'New Signal':
                self.signal_selector.options = [option for option in list(self.signal_selector.options) if option != 'New Signal']
                if len(self.signal_selector.options) > 0:
                    self.signal_selector.value = self.signal_selector.options[0]
            return
        currdict = dict(self.state.custom_signals)
        del currdict[t]
        self.state.custom_signals = currdict
        self.signal_selector.options = [option for option in list(self.signal_selector.options) if option != t]
        if len(self.signal_selector.options) > 0:
            self.signal_selector.value = self.signal_selector.options[0]

    @pn.depends('signal_selector.value', watch=True)
    def load_signal(self):

        # if not self.signal_selector.value:
        #     print("nothing")
        #     return
        print("SPERM")

        if self.signal_selector.value and self.signal_selector.value in self.state.custom_signals:
            signal_data = self.state.custom_signals[self.signal_selector.value]
            print("SPERM2")
        else:
            signal_data = {
                'value_formula': '',
                'value_colormap': 'coolwarm',
                'value_lb': 0,
                'value_cb': 50,
                'value_ub': 100,
                'border_formula': '',
                'border_colormap': 'None',
                'border_lb': 0,
                'border_cb': 50,
                'border_ub': 100,
                'bold_formula': '',
                'custom': True
            }
            print("SPERM3", self.signal_selector.value)

        print("Signal Data", "\n")
        print(signal_data)

        self.signal_name.value = self.signal_selector.value if self.signal_selector.value else ''
        self.value_formula.value = signal_data['value_formula']
        self.value_colormap.value_name = signal_data['value_colormap']
        self.value_lb.value = signal_data['value_lb']
        self.value_cb.value = signal_data['value_cb']
        self.value_ub.value = signal_data['value_ub']
        self.border_formula.value = signal_data['border_formula']
        self.border_colormap.value = signal_data['border_colormap']
        self.border_lb.value = signal_data['border_lb']
        self.border_cb.value = signal_data['border_cb']
        self.border_ub.value = signal_data['border_ub']
        self.bold_formula.value = signal_data['bold_formula']

        # print("VALCOLORMAP", self.value_colormap.value)

        if not signal_data['custom']:
            self.signal_name.disabled = True
            self.value_formula.disabled = True
            self.delete_button.disabled = True
        else:
            self.signal_name.disabled = False
            self.value_formula.disabled = False
            self.delete_button.disabled = False


    @param.depends('state.custom_signals', 'signal_selector.value', watch=True)
    def refresh(self):
        print("NAIL", self.state.custom_signals, self.signal_selector.value)
        if self.signal_selector.value in self.state.custom_signals:
            self.mypane.object = self.state.custom_signals[self.signal_selector.value]
        else:
            self.mypane.object = {}

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
            pn.pane.Markdown("## Signal Maker"),
            pn.Row(
                pn.Column(
                    self.signal_selector,
                    self.mypane,
                    self.new_signal_button,
                    width=400
                ),
                pn.Column(
                    pn.pane.Markdown("### Signal Name"),
                    self.signal_name,
                    value_section,
                    border_section,
                    bold_section,
                    pn.Row(
                        self.save_button,
                        self.delete_button
                    )
                )
            )
        )
        return self.modal