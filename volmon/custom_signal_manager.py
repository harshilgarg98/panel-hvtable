import param as pm
import panel as pn
import pandas as pd

class SymbolSelector(pm.Parameterized):
    trader_buckets = pm.List([])
    sectors = pm.List([])

    def __init__(self, **params):
        super().__init__(**params)

        self.trader_selector = pn.widgets.MultiChoice(
            name='Trader Bucket Label',
            options=self.trader_buckets,
            value=[],
            width=600
        )
        self.sector_selector = pn.widgets.MultiChoice(
            name='Sector',
            options=self.sectors,
            value=[],
            width=600
        )
        self.additional_symbols JZZJJJJSAAAAA