import pandas as pd
from ta.volatility import BollingerBands
from ta.momentum import RSIIndicator
from ta.utils import dropna

# Define your custom class
class StockData:
    def __init__(self, epoch_time, open_value, highest_value, lowest_value, close_value, volume):
        self.epoch_time = epoch_time
        self.open = open_value
        self.high = highest_value
        self.low = lowest_value
        self.close = close_value
        self.volume = volume

def convert_df(data):


    # data = [[1721881800, 24273.15, 24303.15, 24267.7, 24294.95, 0], [1721882700, 24294.8, 24307.9, 24270.85, 24278.7, 0], [1721883600, 24278.3, 24327.2, 24277.15, 24317.8, 0], [1721884500, 24317.2, 24330.1, 24305.2, 24320.2, 0], [1721885400, 24318.8, 24332.45, 24309.8, 24324.2, 0], [1721886300, 24324.05, 24333.35, 24295.1, 24329, 0], [1721887200, 24328.45, 24344.95, 24326.7, 24337.65, 0], [1721888100, 24337, 24366.5, 24333.95, 24358.2, 0], [1721889000, 24357.4, 24368.65, 24345.75, 24362.95, 0], [1721889900, 24362.15, 24379.2, 24358.9, 24370.3, 0], [1721890800, 24369.85, 24376.65, 24354.7, 24358.45, 0], [1721891700, 24358.4, 24395.05, 24357.25, 24390.95, 0], [1721892600, 24390.7, 24397.9, 24381.15, 24382.3, 0], [1721893500, 24381.8, 24396.95, 24380.3, 24392.3, 0], [1721894400, 24392.15, 24394.1, 24361.05, 24367.1, 0], [1721895300, 24366, 24395.5, 24364.4, 24394.4, 0], [1721896200, 24394.2, 24426.15, 24392.6, 24421.35, 0], [1721897100, 24422.45, 24424.65, 24405.7, 24414.5, 0], [1721898000, 24415.15, 24419.95, 24380.1, 24382.25, 0], [1721898900, 24383.25, 24412.1, 24382.15, 24399.8, 0], [1721899800, 24400.55, 24411.25, 24389.3, 24397.5, 0], [1721900700, 24396.5, 24423.15, 24388.95, 24415, 0], [1721965500, 24423.35, 24492.7, 24410.9, 24477.2, 0], [1721966400, 24477.65, 24528.95, 24462, 24526.6, 0], [1721967300, 24526.4, 24551.65, 24511.45, 24548.85, 0], [1721968200, 24548.65, 24595, 24548, 24578.7, 0], [1721969100, 24578.45, 24610.15, 24576.25, 24590.85, 0], [1721970000, 24590.65, 24609.2, 24590.05, 24598.95, 0], [1721970900, 24599.05, 24615.1, 24590.1, 24613.25, 0], [1721971800, 24613.35, 24654.45, 24610.6, 24644.8, 0], [1721972700, 24643.95, 24655.55, 24637.65, 24639.55, 0], [1721973600, 24639.95, 24643.8, 24623.6, 24635.75, 0], [1721974500, 24635.6, 24656.85, 24634.3, 24651.05, 0], [1721975400, 24650.8, 24653.85, 24638.5, 24639, 0], [1721976300, 24638.95, 24656.05, 24637.1, 24650.85, 0], [1721977200, 24651, 24721.5, 24648.35, 24718.65, 0], [1721978100, 24718.15, 24733.3, 24711.35, 24716.35, 0], [1721979000, 24715.85, 24781.15, 24715.85, 24775.55, 0], [1721979900, 24777.1, 24802.15, 24758.2, 24783.75, 0], [1721980800, 24781.8, 24814.25, 24776.55, 24795.55, 0], [1721981700, 24794.45, 24818.25, 24758.35, 24790.1, 0], [1721982600, 24787.35, 24800.15, 24766.25, 24797.8, 0], [1721983500, 24797.75, 24807.2, 24759.45, 24783.6, 0], [1721984400, 24783.25, 24808.4, 24778.6, 24801.45, 0], [1721985300, 24800.25, 24834.15, 24797, 24828.35, 0], [1721986200, 24827.1, 24853.1, 24810.75, 24849.05, 0], [1721987100, 24848, 24861.15, 24830.4, 24851.75, 0]]

    stock_objects = []
    for x in data:
        stock_objects.append(StockData(x[0], x[1], x[2], x[3], x[4], x[5]))


    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame([vars(stock) for stock in stock_objects])

    print(df.head())

    df['date'] = pd.to_datetime(df['epoch_time'], unit='s')
    df['date'] = df['date'].dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')


    df.to_csv('stock_data.csv', index=False)  # Specify the desired file name

def add_bb():
    df = pd.read_csv('stock_data.csv')
    # Initialize Bollinger Bands Indicator
    indicator_bb = BollingerBands(close=df["close"], window=20, window_dev=2)

    # Add Bollinger Bands features
    df['bb_bbm'] = indicator_bb.bollinger_mavg()
    df['bb_bbh'] = indicator_bb.bollinger_hband()
    df['bb_bbl'] = indicator_bb.bollinger_lband()

    # Add Bollinger Band high indicator
    df['bb_bbhi'] = indicator_bb.bollinger_hband_indicator()

    # Add Bollinger Band low indicator
    df['bb_bbli'] = indicator_bb.bollinger_lband_indicator()
    
    df.to_csv('stock_bb.csv', index=False)

    print(df.head(15))

    
def add_rsi():
    df = pd.read_csv('stock_data.csv')

    
    indicator_rsi = RSIIndicator(close=df["close"], window=14)
    df['rsi'] = indicator_rsi.rsi()
    df.to_csv('stock_rsi.csv', index=False)

    print(df.head(15))

add_rsi()
add_bb()