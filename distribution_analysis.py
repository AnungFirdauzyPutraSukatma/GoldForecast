import pandas as pd
import numpy as np


class DistributionAnalysis:

    def __init__(
        self,
        time_bars,
        tick_volume_bars
    ):

        self.time_bars = time_bars.copy()
        self.tick_volume_bars = tick_volume_bars.copy()

    def _calculate_return_stats(
        self,
        data
    ):

        returns = (
            data['CLOSE']
            .pct_change()
            .dropna()
        )

        mean_return = returns.mean()

        std_return = returns.std()

        cv = np.nan

        if mean_return != 0:

            cv = (
                abs(std_return)
                /
                abs(mean_return)
            )

        return {

            'Mean Return':
            mean_return,

            'Std Return':
            std_return,

            'CV Return':
            cv

        }

    def process(self):

        required_columns = [
            'CLOSE'
        ]

        for col in required_columns:

            if col not in self.time_bars.columns:

                raise KeyError(
                    f'Kolom {col} tidak ditemukan pada Time Bars'
                )

            if col not in self.tick_volume_bars.columns:

                raise KeyError(
                    f'Kolom {col} tidak ditemukan pada Tick Volume Bars'
                )

        time_stats = (
            self._calculate_return_stats(
                self.time_bars
            )
        )

        tick_stats = (
            self._calculate_return_stats(
                self.tick_volume_bars
            )
        )

        result = pd.DataFrame({

            'Statistic': [

                'Mean Return',
                'Std Return',
                'CV Return'

            ],

            'Time Bars': [

                time_stats['Mean Return'],
                time_stats['Std Return'],
                time_stats['CV Return']

            ],

            'Tick Volume Bars': [

                tick_stats['Mean Return'],
                tick_stats['Std Return'],
                tick_stats['CV Return']

            ]

        })

        print('\n===== DISTRIBUTION ANALYSIS =====\n')

        print(
            result.to_string(
                index=False
            )
        )

        if (
            tick_stats['CV Return']
            <
            time_stats['CV Return']
        ):

            print(
                '\nTick Volume Bars memiliki CV lebih rendah '
                '(distribusi lebih stabil).'
            )

        elif (
            tick_stats['CV Return']
            >
            time_stats['CV Return']
        ):

            print(
                '\nTime Bars memiliki CV lebih rendah '
                '(distribusi lebih stabil).'
            )

        else:

            print(
                '\nCV kedua metode sama.'
            )

        result.to_csv(
            'distribution_analysis.csv',
            index=False
        )
        return result