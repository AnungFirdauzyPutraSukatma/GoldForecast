import pandas as pd


class CategorizationProcessor:

    def __init__(self, data):

        if isinstance(data, pd.DataFrame):
            self.data = data.copy()

        else:
            raise TypeError(
                "Input harus berupa DataFrame"
            )

    def process(self):

        # ==========================
        # RSI
        # ==========================

        self.data['RSI'] = self.data['RSI'].apply(
            self._categorize_rsi
        )

        # ==========================
        # STOCHASTIC
        # ==========================

        self.data['STOCH_D'] = self.data[
            'STOCH_D'
        ].apply(
            self._categorize_stochastic
        )

        # ==========================
        # MACD Histogram
        # ==========================

        self.data['MACD_HIST'] = self.data[
            'MACD_HIST'
        ].apply(
            self._categorize_macd
        )

        # ==========================
        # ATR
        # ==========================

        self.data['ATR'] = (
            self.data['ATR']
            .round(3)
        )

        self.data.to_csv("Data dengan Kelas Indikator.csv",index=True)

        return self.data

    # ==========================
    # Fungsi Kategorisasi RSI
    # ==========================

    def _categorize_rsi(self, value):

        if value > 70:
            return 'OVERBOUGHT'

        elif value < 30:
            return 'OVERSOLD'

        else:
            return 'NEUTRAL'

    # ==========================
    # Fungsi Kategorisasi STOCH
    # ==========================

    def _categorize_stochastic(self, value):

        if value > 70:
            return 'OVERBOUGHT'

        elif value < 30:
            return 'OVERSOLD'

        else:
            return 'NEUTRAL'

    # ==========================
    # Fungsi Kategorisasi MACD
    # ==========================

    def _categorize_macd(self, value):

        if value > 0:
            return 'BULLISH'

        elif value < 0:
            return 'BEARISH'

        else:
            return 'SIDEWAYS'