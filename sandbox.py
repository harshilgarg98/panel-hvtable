# import panel as pn

# # Initialize Panel
# pn.extension()

# # Create a TextInput widget
# text_input = pn.widgets.TextInput(name="Enter some text", value="")

# # Create a function to display the input value
# @pn.depends(text_input.param.value_input)
# def display_value(value_input):
#     return f"You entered: {value_input}"

# # Create a layout
# layout = pn.Column(
#     text_input,
#     pn.pane.Markdown("## Input Value:"),
#     display_value
# )

# # Show the app
# layout.servable()

##########

# import panel as pn
# #import hvplot.pandas  # noqa
# import pandas as pd

# from panel_modal import Modal

# pn.extension("modal", sizing_mode="stretch_width")

# age_list = [8, 10, 12, 14, 72, 74, 76, 78, 20, 25, 30, 35, 60, 85]
# df = pd.DataFrame({"gender": list("MMMMMMMMFFFFFF"), "age": age_list})
# # plot = df.hvplot.box(y='age', by='gender', height=400, width=400, legend=False, ylim=(0, None))

# content = pn.Column(
#     "## Hi. I'm a *modal*"  , sizing_mode="fixed", width=600
# )
# modal = Modal(content)

# layout = pn.Column(modal.param.open, modal, modal.param.is_open, modal.param.show_close_button)

# pn.template.FastListTemplate(
#     site="Awesome Panel", site_url="./",
#     title="Panel Modal",
#     favicon="https://raw.githubusercontent.com/MarcSkovMadsen/awesome-panel-assets/320297ccb92773da099f6b97d267cc0433b67c23/favicon/ap-1f77b4.ico",
#     main=[__doc__, layout]
# ).servable()

##########

# from datetime import datetime
# from time import sleep

# import panel as pn

# pn.extension()

# def get_data():
#     print("loading data ...")
#     sleep(10)
#     return {"last_update": str(datetime.now())}

# get_data_cached = pn.cache(get_data)

# data = get_data_cached()

# pn.pane.JSON(data).servable()

##########
# import panel as pn
# import time

# pn.extension(nthreads=8)

# def button_click(event):
#     print(f'Button clicked for the {event.new}th time.')
#     time.sleep(2) # Simulate long running operation
#     print(f'Finished processing {event.new}th click.')

# button = pn.widgets.Button(name='Click me!')

# button.on_click(button_click)

# pn.Column(button).servable()


# from time import sleep

# import panel as pn

# pn.extension()

# @pn.cache
# def algo(value):
#     print(f"calculating {value}")
#     sleep(1)
#     return value

# slider = pn.widgets.IntSlider(name="Value", value=2, start=0, end=10)
# pn.Column(
#     slider, pn.bind(algo, slider)
# ).servable()


# import panel as pn
# import time
# run = pn.widgets.Button(name="Press to run calculation", align='center')

# def runner(run):
#     if not run:
#         yield "Calculation did not run yet"
#         return
#     for i in range(101):
#         time.sleep(0.01) # Some calculation
#         yield pn.Column(
#             f'Running ({i}/100%)', pn.indicators.Progress(value=i)
#         )
#     yield "Success ✅︎"
# pn.Row(run, pn.bind(runner, run)).servable()

# import panel as pn
# import param

# # Enable the PyScript extension for Panel
# pn.extension(sizing_mode="stretch_width")

# # Create a text input widget
# text_input = pn.widgets.TextInput(name="Enter text", value="")
# mylist = [1,2,3]

# # Create a function to display the input value
# # @pn.depends(text_input.param.value_input)
# def display_value(text):
#     return f"You entered: {text}"

# # Create the layout
# layout = pn.Column(
#     text_input,
#     mylist,
#     pn.bind(display_value, text_input.param.value_input, watch=True),
#     #mylist
# )

# # Serve the application
# layout.servable()

# import panel as pn

# pn.extension()

# submit = pn.widgets.Button(name="Start the wind turbine")

# def start_stop_wind_turbine(clicked):
#     print(submit.clicks)
#     if submit.clicks % 2 == 0:
#         print("X")
#         submit.name = "Start the wind turbine"
#     else:
#         submit.name = "Stop the wind turbine"


# pn.Column(submit,pn.bind(start_stop_wind_turbine, submit)).servable()



# import panel as pn
# pn.extension()

# def callback(event):
#     print("SCAB")
#     return event

# button = pn.widgets.Button(name="Scab")
# counter = pn.bind(callback, button)
# pn.Row(counter, button).servable()







# import panel as pn
# import param

# pn.extension()

# class Dummy(param.Parameterized):
#     data = param.Dict()

#     def __init__(self, **params):
#         super().__init__(**params)
#         self.input = pn.widgets.TextInput(name='DataInput', value="")
#         self.btn = pn.widgets.Button(name='btn', button_type='primary')
#         #self.pane = pn.pane.JSON(self.data, name='XX')

#         self.btn.on_click(self.update_data)

#     def update_data(self, event):
#         currdict = dict(self.data)
#         currdict['msg'] = {
#             'wire': self.input.value
#         }
#         self.data = currdict
#         #self.pane.object = self.data

#     def view(self):
#         return pn.Column(
#             self.input,
#             self.btn,
#             self.data,
#             #self.pane
#         )

# arr = Dummy(data=dict())
# app = pn.Column(arr.view)
# app.servable()




# import panel as pn
# import colorcet as cc

# from panel_modal import Modal

# pn.extension()
# pn.extension("modal")

# print(cc.palette)

# r = pn.Column(pn.widgets.Select(options=cc.palette))
# modal = Modal(r)

# pn.Column(
#     modal.param.open,
#     modal
# ).servable()

# confetti.py



# import panel as pn
# import param

# from panel.custom import ReactComponent


# class CounterButton(ReactComponent):

#     value = param.Integer()

#     _esm = """
#     export function render({model}) {
#       const [value, setValue] = model.useState("value");
#       return (
#         <button onClick={e => setValue(value+1)}>
#           count is {value}
#         </button>
#       )
#     }
#     """

# CounterButton().servable()

# import random
# import pandas as pd
# import param
# import panel as pn

# from panel.custom import PaneBase, ReactComponent

# class GridJS(ReactComponent):
#     _esm = """
#     import { useEffect, useState } from "react"
#     export function render() {
#       return (
#         <div className="p-4 bg-blue-100 rounded-md">
#           <h1 className="text-xl font-bold mb-2">Hello, React!</h1>
#           <p className="text-gray-700">This is a super simple React component.</p>
#         </div>
#       );
#     };
#     """

#     __css__ = [
#       "https://unpkg.com/gridjs/dist/theme/mermaid.min.css",
#       "https://cdn.tailwindcss.com"
#     ]


# update_button = pn.widgets.Button(name="UPDATE", button_type="primary")

# grid = GridJS()

# pn.Column(update_button, grid).servable()

# import panel as pn
# import pandas as pd
# import numpy as np
# import colorcet as cc
# from bokeh.colors import RGB

# # Enable the tabulator extension
# pn.extension('tabulator')

# # Create sample data
# np.random.seed(42)
# data = pd.DataFrame({
#     'Name': [f'Person {i}' for i in range(1, 11)],
#     'Age': np.random.randint(20, 60, 10),
#     'Score': np.random.randint(0, 101, 10)
# })

# # Define a function to apply gradient coloring using colorcet
# def color_gradient(value, lower, center, upper, palette_name='fire'):
#     palette = cc.palette[palette_name]
#     if value <= lower:
#         idx = 0
#     elif value >= upper:
#         idx = len(palette) - 1
#     elif value < center:
#         idx = int((value - lower) / (center - lower) * len(palette) / 2)
#     else:
#         idx = int(len(palette) / 2 + (value - center) / (upper - center) * len(palette) / 2)
    
#     color = RGB(*[int(c * 255) for c in palette[idx]])
#     return f'background-color: {color}; color: white'

# # Create widgets for user input
# lower_bound = pn.widgets.IntSlider(name='Lower Bound', start=0, end=100, value=0)
# center_bound = pn.widgets.IntSlider(name='Center Bound', start=0, end=100, value=50)
# upper_bound = pn.widgets.IntSlider(name='Upper Bound', start=0, end=100, value=100)
# palette_select = pn.widgets.Select(name='Color Palette', options=['fire', 'bgy', 'coolwarm', 'rainbow'], value='fire')

# # Create the tabulator widget
# tabulator = pn.widgets.Tabulator(
#     data,
#     header_align='center',
#     show_index=False,
#     formatters={
#         'Score': {'type': 'progress', 'color': ['red', 'orange', 'green']},
#     }
# )

# # Function to update the tabulator styles
# def update_styles(event):
#     tabulator.styles = {
#         'Score': lambda v: color_gradient(v, lower_bound.value, center_bound.value, upper_bound.value, palette_select.value)
#     }

# # Add callbacks to update the tabulator when inputs change
# lower_bound.param.watch(update_styles, 'value')
# center_bound.param.watch(update_styles, 'value')
# upper_bound.param.watch(update_styles, 'value')
# palette_select.param.watch(update_styles, 'value')

# # Initial update of styles
# update_styles(None)

# # Create a panel layout
# layout = pn.Column(
#     pn.pane.Markdown("# Gradient-Shaded Tabulator Example with Colorcet"),
#     pn.Row(lower_bound, center_bound, upper_bound, palette_select),
#     tabulator
# )

# # Show the panel
# layout.servable()

# import pandas as pd
# import numpy as np
# import panel as pn
# import colorcet as cc
# from bokeh.models import LinearColorMapper
# from bokeh.palettes import RdBu11

# # Enable Panel extensions
# pn.extension('tabulator')

# # Create sample data
# np.random.seed(42)
# data = pd.DataFrame({
#     'A': np.random.rand(100),
#     'B': np.random.randint(0, 100, 100),
#     'C': np.random.choice(['X', 'Y', 'Z'], 100),
#     'D': np.random.normal(0, 1, 100)
# })

# # Create a color mapper
# color_mapper = LinearColorMapper(palette=RdBu11, low=data['A'].min(), high=data['A'].max())

# # Define the formatter function
# def coolwarm_formatter(value):
#     if pd.isna(value):
#         return ''
#     color = color_mapper.palette[int((value - color_mapper.low) / (color_mapper.high - color_mapper.low) * (len(color_mapper.palette) - 1))]
#     return f'background-color: #{color[1:]}; color: {"black" if sum(int(color[i:i+2], 16) for i in (1, 3, 5)) > 384 else "white"}'

# # Apply the formatter to the entire DataFrame
# styled_df = data.style.applymap(coolwarm_formatter, subset=['A'])

# # Create the tabulator
# tabulator = pn.widgets.Tabulator(
#     styled_df,
#     width=800,
#     height=400
# )

# # Create a layout
# layout = pn.Column(
#     pn.pane.Markdown("# Panel Tabulator with Coolwarm Colormap"),
#     tabulator
# )

# # Show the layout
# layout.servable()


import pandas as pd
import numpy as np
import panel as pn
import colorcet as cc
from bokeh.models import LinearColorMapper
# from bokeh.palettes import RdBu11, PiYG256

# Enable Panel extensions
pn.extension('tabulator')

# Create sample data
np.random.seed(42)
data = pd.DataFrame({
    'A': np.random.rand(100),
    'B': np.random.randint(0, 100, 100),
    'C': np.random.choice(['X', 'Y', 'Z'], 100),
    'D': np.random.normal(0, 1, 100)
})

lb = -1
cb = 0
ub = 1

# Create a color mapper
color_mapper = LinearColorMapper(palette=cc.coolwarm, low=lb, high=ub)

print(
  color_mapper.palette[0],
  color_mapper.palette[127],
  color_mapper.palette[255]
)

def vectorized_linear_map(value, lower, center, upper):
  return np.select(
    condlist = [
      value <= lower,
      value >= upper,
      value <= center,
      value >= center
    ],
    choicelist = [
      0,
      255,
      (127 * (value - lower) / (center - lower)).astype(int),
      (127 + 128 * (value - center) / (upper - center)).astype(int)
    ]
  )

# Define the formatter function
def colorer(value):
    print("HELLO", value)
    print(vectorized_linear_map(value, lb, cb, ub))

    #return [f'background-color:{color_mapper.palette[t]}' for t in vectorized_linear_map(value, lb, cb, ub)]

    # color = color_mapper.palette[linear_map(value, lb, cb, ub)]
    return [
      f'background-color:{color_mapper.palette[t]}; color: {"black" if sum(int(color_mapper.palette[t][i:i+2], 16) for i in (1, 3, 5)) > 384 else "white"}'
      for t in vectorized_linear_map(value, lb, cb, ub)
    ]

# Apply the formatter to the entire DataFrame
styled_df = data.style.apply(colorer, subset=['D'])

# Create the tabulator
tabulator = pn.widgets.Tabulator(
    styled_df,
    width=800,
    height=400
)

# Create a layout
layout = pn.Column(
    pn.pane.Markdown("# Panel Tabulator with Coolwarm Colormap"),
    tabulator
)

# Show the layout
layout.servable()