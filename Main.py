import pandas as pd
from GetDailyEMA import TickVolumeProcessor
from tick_volume_bars import TickVolumeBars
from indicator import IndicatorProcessor
from Kategorisasi import CategorizationProcessor
from labeling import TripleBarrierLabeling
from naive_bayes_model import NaiveBayesModel
from time_based_bars import TimeBasedBars
from distribution_analysis import DistributionAnalysis

def Raw_Data(file_path: str, sheet_name=0):

    if file_path.endswith('.csv'):
        tabel = pd.read_csv(file_path, sep='\t')

    elif file_path.endswith(('.xlsx', '.xls')):
        tabel = pd.read_excel(file_path, sheet_name=sheet_name)

    else:
        raise ValueError('Format file tidak didukung')

    return tabel



# Contoh penggunaan
if __name__ == '__main__':
    data = Raw_Data('Data_Raw.csv')
    thresshold = TickVolumeProcessor('Data_Raw.csv')

    builder = TickVolumeBars(
        data_h1=data,
        data_threshold=thresshold,
        threshold_column='EMA_TICKVOL_20_HARI'
    )

    tick_volume_bars = builder.process()

    raw_indicator = IndicatorProcessor(tick_volume_bars)

    raw_final_data = (raw_indicator.process())

    categorize_data = CategorizationProcessor(raw_final_data)

    final_data = categorize_data.process()

    labeler = TripleBarrierLabeling(
        final_data,
        horizon=12,
        atr_multiplier=2,
        output_file='dataset.csv'
    )

    dataset = labeler.process()

    bayes = NaiveBayesModel(dataset)
    result = bayes.process()



    
    # Tick Volume Based Bars
    print('Data berhasil disimpan ke variabel')
    print(data.head())
    print(len(data))
    print(tick_volume_bars.head())
    print(len(tick_volume_bars))
    print(
        tick_volume_bars[
            'CANDLE_COUNT'
        ].describe()
    )
    print(
        tick_volume_bars[
            'CANDLE_COUNT'
        ].value_counts()
    )
    print(raw_final_data.head())
    print(final_data.head())
    print(
        final_data['RSI']
        .value_counts()
    )
    print(
        final_data['STOCH_D']
        .value_counts()
    )
    print(
        final_data['MACD_HIST']
        .value_counts()
    )
    print(
        dataset['LABEL']
        .value_counts()
    )
    print(dataset['RSI'].value_counts())
    print(dataset['STOCH_D'].value_counts())
    print(dataset['MACD_HIST'].value_counts())
    print(dataset.head())
    print(
        dataset.groupby(
        [
            'LABEL',
            'RSI',
            'STOCH_D',
            'MACD_HIST'
        ]
        ).size()
        .sort_values(
            ascending=False
        )
    )

    # TIME_BASED_BARS

    builder = TimeBasedBars(
        data
    )
    print(data.columns.tolist())

    time_bars = builder.process()

    raw_indicator = IndicatorProcessor(
        time_bars
    )

    raw_final_data = (
        raw_indicator.process()
    )

    categorize_data = CategorizationProcessor(
        raw_final_data
    )

    final_data = (
        categorize_data.process()
    )

    labeler = TripleBarrierLabeling(

        final_data,

        horizon=12,

        atr_multiplier=2,

        output_file='dataset_timebars.csv'

    )

    dataset = labeler.process()

    bayes = NaiveBayesModel(
        dataset
    )

    result = bayes.process()



    time_builder = TimeBasedBars(data)

    time_bars = (
        time_builder.process()
    )

    distribution = DistributionAnalysis(
        time_bars,
        tick_volume_bars
    )

    distribution_result = (
        distribution.process()
    )

    

    

