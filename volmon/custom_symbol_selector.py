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
        self.additional_symbols = pn.widgets.TextInput(name='Additional Symbols', width=600)
        self.excluded_symbols = pn.widgets.TextInput(name='Excluded Symbols', width=600)

    def filter_symbols(self, df):
        ds = df.copy()
        
        if self.trader_selector.value:
            ds = ds[ds['TraderBucketLabel'].isin(self.trader_selector.value)]
        if self.sector_selector.value:
            ds = ds[ds['Sector'].isin(self.sector_selector.value)]
        if self.additional_symbols.value_input:
            additional_symbols = [s.strip() for s in self.additional_symbols.value_input.split(',')]
            additional_rows = df[df['Symbol'].isin(additional_symbols)]
            ds = pd.concat([ds, additional_rows]).drop_duplicates()
        if self.excluded_symbols.value_input:
            excluded_symbols = [s.strip() for s in self.excluded_symbols.value_input.split(',')]
            ds = ds[~ds['Symbol'].isin(excluded_symbols)]

        return ds

    def view(self):
        return pn.Column(
            "## Symbol Selector",
            self.trader_selector,
            self.sector_selector,
            self.additional_symbols,
            self.excluded_symbols,
            sizing_mode="stretch_width",
            width=1000
        )
