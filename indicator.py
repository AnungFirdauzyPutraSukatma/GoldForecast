import pandas as pd


class IndicatorProcessor:

    def __init__(self, data):

        if isinstance(data, pd.DataFrame):
            self.data = data.copy()

        else:
            raise TypeError(
                "Input harus berupa DataFrame"
            )

    def process(self):

        # ==================================
        # RSI (14)
        # ==================================

        delta = self.data['CLOSE'].diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(
            window=5
        ).mean()

        avg_loss = loss.rolling(
            window=5
        ).mean()

        rs = avg_gain / avg_loss

        self.data['RSI'] = (
            100 - (100 / (1 + rs))
        )

        # ==================================
        # STOCHASTIC %D (14,3,3)
        # ==================================

        lowest_low = (
            self.data['LOW']
            .rolling(14)
            .min()
        )

        highest_high = (
            self.data['HIGH']
            .rolling(14)
            .max()
        )

        stoch_k = (

            (
                self.data['CLOSE']
                - lowest_low
            )

            /

            (
                highest_high
                - lowest_low
            )

        ) * 100

        self.data['STOCH_D'] = (
            stoch_k
            .rolling(3)
            .mean()
        )

        # ==================================
        # MACD HISTOGRAM (12,26,9)
        # ==================================

        ema_fast = (
            self.data['CLOSE']
            .ewm(
                span=12,
                adjust=False
            )
            .mean()
        )

        ema_slow = (
            self.data['CLOSE']
            .ewm(
                span=26,
                adjust=False
            )
            .mean()
        )

        macd = (
            ema_fast
            - ema_slow
        )

        macd_signal = (
            macd
            .ewm(
                span=9,
                adjust=False
            )
            .mean()
        )

        self.data['MACD_HIST'] = (
            macd
            - macd_signal
        )

        # ==================================
        # ATR (14)
        # ==================================

        prev_close = (
            self.data['CLOSE']
            .shift(1)
        )

        tr1 = (
            self.data['HIGH']
            -
            self.data['LOW']
        )

        tr2 = abs(
            self.data['HIGH']
            -
            prev_close
        )

        tr3 = abs(
            self.data['LOW']
            -
            prev_close
        )

        true_range = pd.concat(
            [tr1, tr2, tr3],
            axis=1
        ).max(axis=1)

        self.data['ATR'] = (
            true_range
            .rolling(14)
            .mean()
        )

        # ==================================
        # Hapus warm-up
        # ==================================

        self.data.dropna(
            inplace=True
        )

        self.data.reset_index(
            drop=True,
            inplace=True
        )

        self.data.to_csv("Data Tick Volume Based Bars dengan Indikator.csv",index=True)

        return self.data