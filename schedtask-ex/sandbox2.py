import panel as pn
import time

# Enable the use of Markdown in text
pn.extension('markdown')

# Initialize the cache
cache = pn.state.cache

# Define a function to get data (simulating a time-consuming operation)
@cache.memoize
def get_data():
    # Simulate a time-consuming operation
    time.sleep(2)
    return "This is cached data!"

# Create a button to trigger data retrieval
update_button = pn.widgets.Button(name="Update Data", button_type="primary")

# Create a text output to display the data
data_output = pn.pane.Markdown("Click the button to load data.")

# Define the update function
def update_data(event):
    data_output.object = f"Loading data..."
    # Use the cached function
    data = get_data()
    data_output.object = f"Data: {data}"

# Attach the update function to the button
update_button.on_click(update_data)

# Create the app layout
app = pn.Column(
    pn.pane.Markdown("# Panel App with Cached Data"),
    update_button,
    data_output
)

# Serve the app
app.servable()