import panel as pn
from tasks import status
import pandas as pd

pn.extension('tabulator')

pn.extension(sizing_mode="stretch_width", template="fast", theme="dark")
pn.state.template.site="Panel"
pn.state.template.title="Non blocking Background tasks using async"

slider = pn.widgets.IntSlider(value=5, start=0, end=10)

if 'df' in pn.state.cache:
    df = pn.state.cache['df']
else:
    df = pd.DataFrame()
table = pn.widgets.Tabulator(df)

# @pn.depends(status.param.df, watch=True)
def reload_df(df):
    k = df.new
    print(k)
    table.value = k

status.param.watch(reload_df, 'df')

pn.Column(
    "# Slider",
    slider, slider.param.value,
    table,
    "# Task Log",
    pn.widgets.TextAreaInput.from_param(status.param.task1_log, height=500),
    """
    Global Tasks are scheduled using `pn.state.schedule_task(name="update-cache", callback=run_task1, period="10s")`
    """
).servable()