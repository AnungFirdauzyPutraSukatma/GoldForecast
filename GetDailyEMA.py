import pandas as pd


class TickVolumeProcessor:

    def __init__(self, file_path, ema_period=20):

        # =========================
        # MEMBACA DATA
        # =========================

        data_h1 = pd.read_csv(
            file_path,
            sep='\t'
        )
        
        # Membersihkan nama kolom
        data_h1.columns = (
            data_h1.columns.str.strip('<>')
        )

        # Konversi datetime
        data_h1['DATETIME'] = pd.to_datetime(
            data_h1['DATE'] + ' ' + data_h1['TIME'],
            format='%Y.%m.%d %H:%M:%S'
        )

        # Konversi tick volume
        data_h1['TICKVOL'] = pd.to_numeric(
            data_h1['TICKVOL'],
            errors='coerce'
        )

        # =========================
        # MEMBUAT DATA DAILY
        # =========================

        data_h1['DAY'] = (
            data_h1['DATETIME'].dt.date
        )

        data_daily = (
            data_h1
            .groupby('DAY')['TICKVOL']
            .sum()
            .reset_index()
        )

        # =========================
        # EMA 20 HARI
        # =========================

        data_daily[
            f'EMA_TICKVOL_{ema_period}_HARI'
        ] = data_daily['TICKVOL'].ewm(
            span=ema_period,
            adjust=False
        ).mean()

        # =========================
        # DROP WARM-UP
        # =========================

        data_daily = (
            data_daily
            .iloc[ema_period:]
            .reset_index(drop=True)
        )

        # Simpan hasil akhir
        self.data = data_daily

        data_daily.to_csv("Data_Daily_Threshold.csv",index=False)


