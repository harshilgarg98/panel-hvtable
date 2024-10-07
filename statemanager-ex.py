import panel as pn
import param
import json
from pathlib import Path

class StateManagementApp(param.Parameterized):
    text_input = param.String(default="")
    slider_value = param.Integer(default=0, bounds=(0, 100))
    checkbox_value = param.Boolean(default=False)
    show_file_input = param.Boolean(default=False)
    
    def __init__(self, **params):
        super().__init__(**params)
        self.export_button = pn.widgets.Button(name="Export State", button_type="primary")
        self.export_button.on_click(self.export_state)
        
        self.import_button = pn.widgets.Button(name="Import State", button_type="primary")
        self.import_button.on_click(self.toggle_file_input)
        
        self.file_input = pn.widgets.FileInput(accept=".json")
        self.import_confirm_button = pn.widgets.Button(name="Confirm Import", button_type="success")
        self.import_confirm_button.on_click(self.import_state)
    
    def export_state(self, event):
        state = {
            "text_input": self.text_input,
            "slider_value": self.slider_value,
            "checkbox_value": self.checkbox_value
        }
        
        # Hardcoded export file location
        file_path = Path.home() / "app_state.json"
        with open(file_path, "w") as f:
            json.dump(state, f)
        
        pn.state.notifications.success(f"State exported to {file_path}", duration=3000)
    
    def toggle_file_input(self, event):
        self.show_file_input = not self.show_file_input
    
    def import_state(self, event):
        if self.file_input.value is not None:
            file_content = self.file_input.value.decode("utf-8")
            state = json.loads(file_content)
            
            self.text_input = state["text_input"]
            self.slider_value = state["slider_value"]
            self.checkbox_value = state["checkbox_value"]
            
            pn.state.notifications.success("State imported successfully", duration=3000)
            self.show_file_input = False
        else:
            pn.state.notifications.error("No file selected", duration=3000)
    
    @pn.depends("text_input", "slider_value", "checkbox_value", "show_file_input")
    def view(self):
        file_input_row = pn.Row(
            self.file_input, 
            self.import_confirm_button, 
            visible=self.show_file_input
        )
        return pn.Column(
            pn.widgets.TextInput.from_param(self.param.text_input),
            pn.widgets.IntSlider.from_param(self.param.slider_value),
            pn.widgets.Checkbox.from_param(self.param.checkbox_value),
            pn.Row(self.export_button, self.import_button),
            file_input_row
        )

app = StateManagementApp()
pn.extension(notifications=True)
pn.panel(app.view).servable()