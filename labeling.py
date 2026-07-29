import pandas as pd


class TripleBarrierLabeling:

    def __init__(
        self,
        data,
        horizon=12,
        atr_multiplier=2,
        output_file='dataset.csv'
    ):

        self.data = data.copy()
        self.horizon = horizon
        self.atr_multiplier = atr_multiplier
        self.output_file = output_file

    def _encode_categories(self, dataset):

        rsi_map = {
            'OVERBOUGHT': 0,
            'OVERSOLD': 1,
            'NEUTRAL': 2
        }

        stochastic_map = {
            'OVERBOUGHT': 0,
            'OVERSOLD': 1,
            'NEUTRAL': 2
        }

        macd_map = {
            'BULLISH': 0,
            'BEARISH': 1,
            'SIDEWAYS': 2
        }

        dataset['RSI'] = dataset['RSI'].map(rsi_map)

        dataset['STOCH_D'] = dataset['STOCH_D'].map(
            stochastic_map
        )

        dataset['MACD_HIST'] = dataset[
            'MACD_HIST'
        ].map(macd_map)

        return dataset

    def process(self):

        required_columns = [

            'RSI',
            'STOCH_D',
            'MACD_HIST',

            'ATR',

            'HIGH',
            'LOW',
            'CLOSE'

        ]

        for column in required_columns:

            if column not in self.data.columns:

                raise KeyError(
                    f'Kolom {column} tidak ditemukan'
                )

        dataset = []

        active_until = -1

        for i in range(
            1,
            len(self.data)
        ):

            # =====================
            # Skip jika event
            # sebelumnya masih aktif
            # =====================

            if i <= active_until:
                continue

            previous_rsi = self.data.loc[
                i - 1,
                'RSI'
            ]

            current_rsi = self.data.loc[
                i,
                'RSI'
            ]

            # =====================
            # RSI pertama kali masuk
            # OVERBOUGHT
            # =====================

            new_overbought = (

                previous_rsi != 'OVERBOUGHT'
                and
                current_rsi == 'OVERBOUGHT'

            )

            # =====================
            # RSI pertama kali masuk
            # OVERSOLD
            # =====================

            new_oversold = (

                previous_rsi != 'OVERSOLD'
                and
                current_rsi == 'OVERSOLD'

            )

            if not (
                new_overbought
                or
                new_oversold
            ):
                continue

            atr = self.data.loc[
                i,
                'ATR'
            ]

            if pd.isna(atr):
                continue

            entry_price = self.data.loc[
                i,
                'CLOSE'
            ]

            upper_barrier = (

                entry_price
                +
                (
                    self.atr_multiplier
                    * atr
                )

            )

            lower_barrier = (

                entry_price
                -
                (
                    self.atr_multiplier
                    * atr
                )

            )

            end_idx = min(
                i + self.horizon,
                len(self.data) - 1
            )

            label = 0

            touched = False

            # =====================
            # Triple Barrier
            # =====================

            for j in range(
                i + 1,
                end_idx + 1
            ):

                future_high = self.data.loc[
                    j,
                    'HIGH'
                ]

                future_low = self.data.loc[
                    j,
                    'LOW'
                ]

                if future_high >= upper_barrier:

                    label = 1

                    touched = True

                    active_until = j

                    break

                if future_low <= lower_barrier:

                    label = -1

                    touched = True

                    active_until = j

                    break

            # =====================
            # Horizon habis
            # =====================

            if not touched:

                active_until = end_idx

            dataset.append({

                'RSI':
                current_rsi,

                'STOCH_D':
                self.data.loc[
                    i,
                    'STOCH_D'
                ],

                'MACD_HIST':
                self.data.loc[
                    i,
                    'MACD_HIST'
                ],

                'LABEL':
                label

            })

        dataset = pd.DataFrame(dataset)

        if len(dataset) == 0:

            raise ValueError(
                'Tidak ada sampel yang berhasil dibuat'
            )

        dataset = self._encode_categories(
            dataset
        )

        dataset.dropna(
            inplace=True
        )

        dataset = dataset.astype({

            'RSI': 'int64',
            'STOCH_D': 'int64',
            'MACD_HIST': 'int64',
            'LABEL': 'int64'

        })

        dataset.reset_index(
            drop=True,
            inplace=True
        )

        dataset.to_csv(
            self.output_file,
            index=False
        )

        print(
            f'Dataset berhasil disimpan ke {self.output_file}'
        )

        print(
            f'Jumlah sampel: {len(dataset)}'
        )

        print(
            '\nDistribusi Label:'
        )

        print(
            dataset['LABEL']
            .value_counts()
            .sort_index()
        )

        dataset.to_csv("Final Dataset.csv",index=True)

        return dataset