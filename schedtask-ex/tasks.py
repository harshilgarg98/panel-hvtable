import asyncio
from datetime import datetime

import panel as pn
import param
import pandas as pd
import numpy as np

class TaskStatus(param.Parameterized):
    task1_log = param.String()
    df = param.DataFrame()

# Create a sample DataFrame
    def __init__(self, **params):
        super().__init__(**params)

        self.df = pd.DataFrame({
            'A': np.random.rand(5),
            'B': np.random.randint(0, 10, 5),
            'C': ['foo', 'bar', 'baz', 'qux', 'quux']
        })

    def reset_dataframe(self):
        self.df = pd.DataFrame({
            'A': np.random.rand(5),
            'B': np.random.randint(0, 10, 5),
            'C': ['foo', 'bar', 'baz', 'qux', 'quux']
        })
        return self.df

# Instantiate the class
status = TaskStatus()

pn.state.cache["value"]=0

async def run_task1():
    status.task1_log += f"{datetime.now():%Y-%m-%d %H:%M:%S} Task 1 started\n"
    proc = await asyncio.create_subprocess_exec(
       'python','task1.py',
       stdout=asyncio.subprocess.PIPE,
       stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()
    if stdout:
        status.task1_log += f"{stdout.decode('utf8')}"
    if stderr:
        status.task1_log += f"{stderr.decode('utf8')}"
    status.task1_log += f"{datetime.now():%Y-%m-%d %H:%M:%S} Task 1 finished\n"
    # Here you could read the task results from stdout, file(s), database or cache
    # and set the cache
    pn.state.cache["value"]+=1

    df = status.reset_dataframe()

    pn.state.cache['df'] = df

    status.task1_log += f"Cache is {pn.state.cache['value']}"


pn.state.schedule_task(name="update-cache", callback=run_task1, period="2s")