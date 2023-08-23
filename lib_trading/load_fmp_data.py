import pandas as pd
import requests
def load_intrinsic_value_fmp(symbol: str) -> float:
    headers= {"user-agent":"Mozilla/5.0"}
    url = "https://site.financialmodelingprep.com/discounted-cash-flow-model-levered/" + str(symbol)
    res = requests.get(url, headers=headers).text
    df= pd.read_html(res)[4]
    return df.iloc[4,1]

def load_multicompanies_intrinsic_value_fmp(lst_symbols: list) -> list:
    list_of_iv = []
    for symbol in lst_symbols:
        list_of_iv.append(load_intrinsic_value_fmp(symbol))
   
    return list_of_iv

def main(lst_symbols: list) -> list:
    return load_multicompanies_intrinsic_value_fmp(lst_symbols)


main(lst_symbols = ['GOOGL', 'MSFT', 'NVDA', 'AAPL', 'META'])


if __name__ == '__main__':
    main()
