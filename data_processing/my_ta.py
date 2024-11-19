import numpy as np
import pandas as pd 

LONG_N = 180
SHORT_N = 30

def get_price_column(df):
    if 'close' in df.columns:
        return 'close'
    elif 'price' in df.columns:
        return 'price'
    else:
        raise ValueError("dataframe needs to have a 'price' or 'close' column")

def volatility(df, long_N=LONG_N, short_N=SHORT_N):
    price_column = get_price_column(df)
    df_copy = df[[price_column]].copy()
    df_copy['log_return'] = np.log(df_copy[price_column] / df_copy[price_column].shift(1))
    df_copy['trailing_volatility_short'] = df_copy['log_return'].rolling(window=short_N).std()
    df_copy['trailing_volatility_long'] = df_copy['log_return'].rolling(window=long_N).std()
    return df_copy[['trailing_volatility_short', 'trailing_volatility_long']]

BB_WINDOW = 20 
BB_MULTIPLIER = 2

def bollinger_bands(df, bb_window=BB_WINDOW, bb_multiplier=BB_MULTIPLIER):
    price_column = get_price_column(df)
    df_copy = df[[price_column]].copy()
    
    df_copy['middle_band'] = df_copy[price_column].rolling(window=bb_window).mean()
    df_copy['std_dev'] = df_copy[price_column].rolling(window=bb_window).std()

    df_copy['upper_band'] = df_copy.middle_band + (bb_multiplier * df_copy.std_dev)
    df_copy['lower_band'] = df_copy.middle_band - (bb_multiplier * df_copy.std_dev)

    df_copy['bb_width'] = df_copy.upper_band / df_copy.lower_band - 1
    df_copy['bb_price'] = (df_copy[price_column] - df_copy.middle_band) / (df_copy.upper_band - df_copy.lower_band)
    df_copy['bb_price_to_lower_band'] = df_copy[price_column] / df_copy.lower_band - 1
    df_copy['bb_price_to_higher_band'] = df_copy[price_column] / df_copy.upper_band
    
    return df_copy[['middle_band', 'upper_band', 'lower_band','bb_width','bb_price', 'bb_price_to_lower_band', 'bb_price_to_higher_band']]


