import pandas as pd
from .indicator import Indicator
from zaifdata.data.prices import get_data_by_count


class RSI(Indicator):
    def __init__(self, currency_pair='btc_jpy', period='1d', length=14):
        super().__init__(currency_pair, period)
        self.length = length

    def request_data(self, count=100, to_epoch_time=None, style='dict'):
        price_data = get_data_by_count(currency_pair=self.currency_pair,
                                       period=self.period,
                                       count=self._get_required_price_count(count),
                                       style='df')

        rsi = self._exec_talib_func(price_data, price='close', timeperiod=self.length)
        formatted_rsi = self._formatting(price_data, rsi, style)
        return formatted_rsi

    @property
    def name(self):
        return 'rsi'

    def _get_required_price_count(self, count):
        return count + self.length

    def _formatting(self, candlesticks, rsi, style):
        rsi.rename(self.name, inplace=True)
        rsi_with_time = pd.concat([candlesticks['time'], rsi], axis=1)
        rsi_with_time.dropna(inplace=True)

        if style == 'df':
            return rsi_with_time.reset_index(drop=True)

        dict_rsi = rsi_with_time.astype(object).to_dict(orient='records')
        return dict_rsi
