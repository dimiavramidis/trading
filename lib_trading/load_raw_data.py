# TODO Load all necessary data to calculate intrinsic value from API, e.g. https://pypi.org/project/reuterspy/ , https://www.macrotrends.net/stocks/charts/GOOGL/alphabet/revenue
## yfinance library
import pandas as pd
import yfinance as yf
import numpy as np

def load_companies_iv_input_data(symbol: str):
    company = yf.Ticker(symbol)

    iv_input = [{
        'freeCashflow': company.info['freeCashflow'], # Free cash flow
        'totalDebt': company.info['totalDebt'], # Total debt
        'totalCash': company.info['totalCash'], # Cash and short term investments
        'sharesOutstanding': company.info['sharesOutstanding'], # No. of outstanding shares
        'beta': company.info['beta'], # Beta
        'previousClose': company.info['previousClose'], # Previous close
        'symbol': company.info['symbol'], # Symbol
        }
        ]

    
    return pd.DataFrame(data = iv_input, columns=['freeCashflow', 'totalDebt', 'totalCash', 'sharesOutstanding','beta', 'previousClose', 'symbol']).set_index('symbol')

# load data from load_companies_iv_input_data() and append to dataframe rowwise iteratively

def load_multicompanies_iv_input_data(lst_symbols: list):

    append_dataframes = []
    for symbol in lst_symbols:
        append_dataframes.append(load_companies_iv_input_data(symbol))
   
    return pd.concat(append_dataframes)

# df_iv = load_multicompanies_iv_input_data(['GOOG', 'MSFT'])


# calculate the free cash flow growth rate for short term, mid term and long term

import requests
import pandas as pd
import numpy as np

def determine_growth_rates(symbol:str)-> pd.DataFrame:

    headers= {"user-agent":"Mozilla/5.0"}
    url_yahoo_finance = "https://sg.finance.yahoo.com/quote/" + str(symbol) + "/analysis?p=" + str(symbol)
    res = requests.get(url_yahoo_finance, headers=headers).text

    df= pd.read_html(res)[5]
    # keep only the first 2 columns
    df = df.iloc[:,0:2]
    # set the index to the first column
    df.set_index(df.columns[0], inplace=True)
    # convert percentage strings to floats and divide by 100
    df = df.apply(lambda x: x.str.strip('%').astype(float)/100, axis=1)
    # rename index to symbol
    df.index.name = 'symbol'
    # transpose the dataframe
    df = df.T
    # deterine the short term growth rate
    df['short_term_growth_rate'] = np.where(((df['Current year'] + df['Next year']) / 2 )< 0.2 , (df['Current year'] + df['Next year']) / 2, 0.20)
    # ((df['Current year'] + df['Next year'])/2, 0.20)
    # deterine the mid term growth rate
    df['mid_term_growth_rate'] = df['Next 5 years (per annum)'] / 2
    # deterine the mid term growth rate
    df['long_term_growth_rate'] = df['mid_term_growth_rate'] / 2
    # change index name to symbol
    df.rename(columns={'index': 'symbol'}, inplace=True)
    # keep column Growth Estimates and Next 5 Years (per annum)
    df = df[['short_term_growth_rate', 'mid_term_growth_rate', 'long_term_growth_rate']]

    return df


def determine_multicompanies_growth_rates(lst_symbols: list):
    append_dataframes = []
    for symbol in lst_symbols:
        append_dataframes.append(determine_growth_rates(symbol))
   
    return pd.concat(append_dataframes, )

def join_iv_input_growth_rates(df_iv_input: pd.DataFrame, df_growth_rates: pd.DataFrame):
    return df_iv_input.join(df_growth_rates, on='symbol')


def main(lst_symbols: list) -> pd.DataFrame:
    df_growth_rates = determine_multicompanies_growth_rates(lst_symbols)
    df_iv_input = load_multicompanies_iv_input_data(lst_symbols)
    df_iv_input_growth_rates = join_iv_input_growth_rates(df_iv_input, df_growth_rates)
    return df_iv_input_growth_rates[['freeCashflow', 'totalDebt', 'totalCash', 'short_term_growth_rate', 'mid_term_growth_rate', 'long_term_growth_rate', 'sharesOutstanding', 'beta', 'previousClose']]

#main(['GOOG', 'MSFT'])
# load_intrinsic_value_financialmodellingprep('GOOGL')
# load_multicompanies_intrinsic_value_financialmodellingprep(['GOOG', 'MSFT'])