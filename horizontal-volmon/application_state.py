import param
import panel as pn

class ApplicationState(param.Parameterized):
    # Symbol manager
    available_trader_buckets = param.List([])
    available_sectors = param.List([])
    selected_trader_buckets = param.List([])
    selected_sectors = param.List([])
    additional_symbols = param.String()
    excluded_symbols = param.String()

    # Signal selector
    available_signals = param.List([])
    selected_signals = param.List([])

    # Main controls -- expiration selector
    available_expirations = param.List([])
    selected_expiration = param.String()

    # Main controls -- grouper
    grouped = param.Boolean()

    # Main controls -- custom filter
    custom_filter = param.String()

    # Custom signals
    custom_signals = param.Dict()

    def __init__(self, **params):
        # self.df = df
        super().__init__(**params)

    #@param.depends('bucket_labels', 'sectors', 'additional_symbols', 'excluded_symbols', watch=True)
    def serialize_state(self):
        return {
            'MainControls': {
                'available_expirations': self.available_expirations,
                'selected_expiration': self.selected_expiration,
                'grouped': self.grouped,
                'custom_filter': self.custom_filter
            },
            'SymbolManager': {
                'available_trader_buckets': self.available_trader_buckets,
                'selected_trader_buckets': self.selected_trader_buckets,
                'available_sectors': self.available_sectors,
                'selected_sectors': self.selected_sectors,
                'additional_symbols': self.additional_symbols,
                'excluded_symbols': self.excluded_symbols
            },
            'SignalSelector': {
                'available_signals': self.available_signals,
                'selected_signals': self.selected_signals,
            },
            'SignalMaker': self.custom_signals
        }
