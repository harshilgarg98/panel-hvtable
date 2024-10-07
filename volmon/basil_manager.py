import asyncio
from datetime import datetime

import panel as pn
import param


class BasilStatus(param.Parameterized):
    task_log = param.String()

status = BasilStatus()

pn.state.cache["value"]=0


import random
import pandas as pd
import numpy as np
import string
TRADER_BUCKETS = ['GARGH', 'FLETCHERMI', 'WANGCLA', 'CHENRYA', 'LIALV', 'JIANGJ']
EXPIRATION_DATES = ['2024-09-06', '2024-09-13', '2024-09-20', '2024-09-27', 
                    '2024-10-04', '2024-10-11', '2024-10-18', '2024-11-15', '2024-12-20']
SECTORS = ['Semiconductors', 'Industrials', 'Travel', 'Software I', 'Software II', 'Materials', 
           'Real Estate', 'Pharmaceuticals', 'Healthcare Services', 'Financial Services', 
           'Consumer Discretionary', 'Communication Services', 'Consumer Staples', 'Utilities']

# Function to generate random 3-character string
def random_symbol():
    return ''.join(random.choices(string.ascii_uppercase, k=3))

async def create_dummy_dataframe(n_rows=100):
    data = {
        "Sector": np.random.choice(SECTORS, n_rows),
        "Symbol": [random_symbol() for _ in range(n_rows)],
        "FairPrice": np.random.uniform(10, 500, n_rows).round(2),
        "SpotReturn": np.random.uniform(-10, 10, n_rows).round(2),
        "TermTotalVol": np.random.uniform(20, 100, n_rows).round(2),
        "Expiration": np.random.choice(EXPIRATION_DATES, n_rows),
        "TraderBucketLabel": np.random.choice(TRADER_BUCKETS, n_rows)
    }
    
    df = pd.DataFrame(data)
    df["Spot1N"] = (df["SpotReturn"] / (df["TermTotalVol"] / 20)).round(4)
    df["BillonSignal"] = np.random.uniform(-5, 5, n_rows).round(2)

    pn.state.cache['df'] = df

    await asyncio.sleep(1)

async def load_data():
    status.task_log += f"{datetime.now():%Y-%m-%d %H:%M:%S} Task 1 started\n"
    await asyncio.run(create_dummy_dataframe)
    status.task_log += f"{datetime.now():%Y-%m-%d %H:%M:%S} Task 1 finished\n"


pn.state.schedule_task(name="load_data", callback=load_data, period="10s")