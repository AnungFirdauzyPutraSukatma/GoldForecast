import pandas as pd


class TickVolumeBars:

    def __init__(
        self,
        data_h1,
        data_threshold,
        threshold_column
    ):

        self.data_h1 = self._extract_dataframe(
            data_h1
        )

        self.data_threshold = self._extract_dataframe(
            data_threshold
        )

        self.threshold_column = threshold_column

        # =========================
        # Bersihkan nama kolom
        # =========================

        self.data_h1.columns = (
            self.data_h1.columns
            .astype(str)
            .str.strip()
            .str.replace('<', '', regex=False)
            .str.replace('>', '', regex=False)
        )

        self.data_threshold.columns = (
            self.data_threshold.columns
            .astype(str)
            .str.strip()
        )

        # =========================
        # Buat DATETIME
        # =========================

        if 'DATETIME' not in self.data_h1.columns:

            if (
                'DATE' in self.data_h1.columns
                and
                'TIME' in self.data_h1.columns
            ):

                self.data_h1['DATETIME'] = pd.to_datetime(
                    self.data_h1['DATE'].astype(str)
                    + ' '
                    +
                    self.data_h1['TIME'].astype(str),
                    format='%Y.%m.%d %H:%M:%S'
                )

            elif 'DATE' in self.data_h1.columns:

                self.data_h1['DATETIME'] = pd.to_datetime(
                    self.data_h1['DATE']
                )

            else:

                raise KeyError(
                    f"""
Kolom DATE/TIME tidak ditemukan.

Kolom tersedia:
{list(self.data_h1.columns)}
"""
                )

        # =========================
        # Pastikan numerik
        # =========================

        numeric_columns = [
            'OPEN',
            'HIGH',
            'LOW',
            'CLOSE',
            'TICKVOL'
        ]

        for col in numeric_columns:

            if col in self.data_h1.columns:

                self.data_h1[col] = pd.to_numeric(
                    self.data_h1[col],
                    errors='coerce'
                )

    # ======================================
    # Mengambil dataframe dari object/class
    # ======================================

    def _extract_dataframe(self, obj):

        if isinstance(obj, pd.DataFrame):
            return obj.copy()

        for attr in [
            'data',
            'result',
            'df',
            'dataframe'
        ]:

            if hasattr(obj, attr):

                value = getattr(
                    obj,
                    attr
                )

                if isinstance(
                    value,
                    pd.DataFrame
                ):
                    return value.copy()

        raise TypeError(
            f"""
Tidak menemukan DataFrame pada object:
{type(obj)}
"""
        )

    # ======================================
    # Proses Tick Volume Bars
    # ======================================

    def process(self):

        # =========================
        # Sinkronisasi tanggal
        # =========================

        self.data_h1['DAY'] = (
            self.data_h1['DATETIME']
            .dt.date
        )

        self.data_threshold['DAY'] = pd.to_datetime(
            self.data_threshold['DAY']
        ).dt.date

        threshold_map = dict(

            zip(

                self.data_threshold['DAY'],

                self.data_threshold[
                    self.threshold_column
                ] / 24

            )

        )

        self.data_h1['THRESHOLD'] = (

            self.data_h1['DAY']
            .map(threshold_map)

        )

        self.data_h1 = self.data_h1.dropna(
            subset=['THRESHOLD']
        )

        # =========================
        # Membentuk Tick Bars
        # =========================

        bars = []

        accumulated_volume = 0
        candle_count = 0

        open_price = None
        high_price = None
        low_price = None

        for _, row in self.data_h1.iterrows():

            if accumulated_volume == 0:

                open_price = row['OPEN']
                high_price = row['HIGH']
                low_price = row['LOW']

                candle_count = 0

            high_price = max(
                high_price,
                row['HIGH']
            )

            low_price = min(
                low_price,
                row['LOW']
            )

            accumulated_volume += row['TICKVOL']

            candle_count += 1

            threshold = row['THRESHOLD']

            if accumulated_volume >= threshold:

                bars.append({

                    'OPEN':
                    open_price,

                    'HIGH':
                    high_price,

                    'LOW':
                    low_price,

                    'CLOSE':
                    row['CLOSE'],

                    'TICKVOL':
                    accumulated_volume,

                    'THRESHOLD':
                    threshold,

                    'CANDLE_COUNT':
                    candle_count

                })

                accumulated_volume = 0

        result = pd.DataFrame(
            bars
        )

        result.reset_index(
            drop=True,
            inplace=True
        )

        result.to_csv("Data_tick_volume_based_bars.csv",index=True)

        return result