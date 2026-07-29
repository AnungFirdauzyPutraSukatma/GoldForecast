import pandas as pd


class TimeBasedBars:

    def __init__(self, data):

        self.data = data.copy()

    def process(self):

        result = pd.DataFrame({

            'OPEN':
            self.data['<OPEN>'],

            'HIGH':
            self.data['<HIGH>'],

            'LOW':
            self.data['<LOW>'],

            'CLOSE':
            self.data['<CLOSE>'],

            'TICKVOL':
            self.data['<TICKVOL>'],

            'THRESHOLD':
            0,

            'CANDLE_COUNT':
            1

        })

        result.reset_index(
            drop=True,
            inplace=True
        )

        return result