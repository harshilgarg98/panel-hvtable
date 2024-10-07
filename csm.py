import panel as pn
import param

class StyleConfigurator(param.Parameterized):
    option = param.ObjectSelector(default='Option 1', objects=['Option 1', 'Option 2', 'Option 3'])

    def __init__(self, **params):
        super().__init__(**params)
        self.state = {}  # We'll only store states that have been explicitly saved

    @param.depends('option', watch=True)
    def _update_form(self):
        self._load_state()

    def _load_state(self):
        if self.option in self.state:
            # Load saved state
            state = self.state[self.option]
            for widget in self.form:
                if isinstance(widget, pn.widgets.Widget):
                    if widget.name in state:
                        widget.value = state[widget.name]
                    else:
                        self._clear_widget(widget)
        else:
            # Clear all inputs if no state is defined
            for widget in self.form:
                if isinstance(widget, pn.widgets.Widget):
                    self._clear_widget(widget)

    def _clear_widget(self, widget):
        if isinstance(widget, pn.widgets.TextInput):
            widget.value = ""
        elif isinstance(widget, pn.widgets.FloatInput):
            widget.value = 0.0
        elif isinstance(widget, pn.widgets.Select):
            widget.value = widget.options[0] if widget.options else None

    def _save_state(self, event):
        self.state[self.option] = {
            widget.name: widget.value 
            for widget in self.form 
            if isinstance(widget, pn.widgets.Widget)
        }
        print(f"State saved for {self.option}")

    def panel(self):
        select = pn.widgets.Select.from_param(self.param.option)

        name_input = pn.widgets.TextInput(name="Name", value="")

        value_section = pn.Column(
            pn.pane.Markdown("### Value / Background Color"),
            pn.widgets.TextInput(name="Value Formula", value=""),
            pn.widgets.Select(name="Value Colormap", options=['viridis', 'plasma', 'inferno', 'magma']),
            pn.Row(
                pn.widgets.FloatInput(name="Value Lower Bound", value=0),
                pn.widgets.FloatInput(name="Value Center", value=50),
                pn.widgets.FloatInput(name="Value Upper Bound", value=100)
            )
        )

        border_section = pn.Column(
            pn.pane.Markdown("### Border"),
            pn.widgets.TextInput(name="Border Formula", value=""),
            pn.widgets.Select(name="Border Colormap", options=['viridis', 'plasma', 'inferno', 'magma']),
            pn.Row(
                pn.widgets.FloatInput(name="Border Lower Bound", value=0),
                pn.widgets.FloatInput(name="Border Center", value=50),
                pn.widgets.FloatInput(name="Border Upper Bound", value=100)
            )
        )

        bold_section = pn.Column(
            pn.pane.Markdown("### Bold"),
            pn.widgets.TextInput(name="Bold Formula", value="")
        )

        save_button = pn.widgets.Button(name="Save", button_type="primary")
        save_button.on_click(self._save_state)

        self.form = pn.Column(
            name_input,
            value_section,
            border_section,
            bold_section,
            save_button
        )

        return pn.Row(select, self.form)

# Create an instance of the StyleConfigurator
configurator = StyleConfigurator()

# Create the panel
panel = configurator.panel()

panel.servable()

# To display the panel, you would typically use:
# panel.show()