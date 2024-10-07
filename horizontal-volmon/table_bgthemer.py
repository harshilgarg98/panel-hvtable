
from bokeh.models import LinearColorMapper

import numpy as np

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
def style_background_color(palette, lower_bound, center_bound, upper_bound):
    color_mapper = LinearColorMapper(palette=palette, low=lower_bound, high=upper_bound)



lb = -1
cb = 0
ub = 1

# Create a color mapper
color_mapper = LinearColorMapper(palette=cc.fire, low=lb, high=ub)

print(
  color_mapper.palette[0],
  color_mapper.palette[127],
  color_mapper.palette[255]
)

def linear_map(value, lower, center, upper):
    if value <= lower:
        return 0
    elif value >= upper:
        return 255
    elif value <= center:
        return int(127 * (value - lower) / (center - lower))
    else:
        return int(127 + 128 * (value - center) / (upper - center))

# Define the formatter function
def coolwarm_formatter(value):
    if pd.isna(value):
        return ''

    color = color_mapper.palette[linear_map(value, lb, cb, ub)]
    return f'background-color:{color}; color: {"black" if sum(int(color[i:i+2], 16) for i in (1, 3, 5)) > 384 else "white"}'

# Apply the formatter to the entire DataFrame
styled_df = data.style.applymap(coolwarm_formatter, subset=['A'])

