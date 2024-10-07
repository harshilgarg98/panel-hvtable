import panel as pn
import pandas as pd
import numpy as np
from datetime import datetime

pn.extension()

class DataManager:
    def __init__(self):
        self.df = self.generate_data()
        self.last_update = pn.widgets.StaticText(name='Last Update', value=self._get_current_time())

    @staticmethod
    def generate_data():
        return pd.DataFrame({
            'A': np.random.rand(5),
            'B': np.random.randint(0, 100, 5),
            'C': np.random.choice(['X', 'Y', 'Z'], 5)
        })

    @staticmethod
    def _get_current_time():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def update_data(self):
        self.df = self.generate_data()
        self.last_update.value = self._get_current_time()
        return self.df  # Return the new DataFrame

class DataframeApp:
    def __init__(self):
        self.data_manager = DataManager()
        self.table = pn.widgets.Tabulator(
            value=self.data_manager.df,
            sizing_mode='stretch_width',
            height=300
        )

    @pn.depends(watch=True)
    def update_table(self):
        new_df = self.data_manager.update_data()
        self.table.value = new_df

    def view(self):
        return pn.Column(
            pn.pane.Markdown("# Periodically Updating DataFrame"),
            self.table,
            self.data_manager.last_update
        )

# Initialize the app
app = DataframeApp()

# Add periodic callback
update_callback = pn.state.add_periodic_callback(app.update_table, period=3000)

# Create the main layout
layout = pn.Column(
    app.view(),
    pn.Param(update_callback, parameters=['period'], name='Update Settings'),
    sizing_mode='stretch_width'
)

# Serve the app
layout.servable()