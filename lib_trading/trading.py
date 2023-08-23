import pandas as pd

from load_raw_data import main as main_load_data
from intrinsic_value import main as main_intrinsic_value
from load_fmp_data import main as load_fmp


def main(lst_symbols: list) -> pd.DataFrame:
    #load input data
    df_iv_input = main_load_data(lst_symbols)
    #calculate intrinsic value for each symbol in index of df_iv_input
    lst_intrinsic_value = []
    for symbol in df_iv_input.index:
        print(symbol)
        lst_intrinsic_value.append(main_intrinsic_value(df_iv_input.loc[symbol]))
    #add intrinsic value to df_iv_input
    df_iv_input['intrinsic_value'] = lst_intrinsic_value
    df_iv_input['discount'] = 1- (df_iv_input['previousClose'] / df_iv_input['intrinsic_value'])
    df_iv_input['intrinsic_value_fmp'] = load_fmp(lst_symbols)
    df_iv_input['discount_fmp'] = 1- (df_iv_input['previousClose'] / df_iv_input['intrinsic_value_fmp'])
    
    return df_iv_input




main(lst_symbols = ['GOOGL', 'MSFT', 'CSCO', 'NVDA', 'INTC', 'AAPL', 'META', 'AVGO'])

