import pandas as pd
import yfinance as yf  #API non officiel -> evite de devoir faire un scrapper

    
def get_data_adj(tickers, start, end, save_to_csv=False):  #Je def source au cas ou pour alternatives Quandl ou Alpha Vantage
    """
    Télécharge les prix ajustés depuis Yahoo Finance
    Args:
        tickers (list): Liste des symboles
        start (str): Date de début (format 'YYYY-MM-DD')
        end (str): Date de fin (format 'YYYY-MM-DD')
        save_to_csv (bool): Si True, sauvegarde les données dans un fichier CSV
    Returns:
        pd.DataFrame: Prix ajustés
    """
    try:
        data = yf.download(tickers, start=start, end=end, auto_adjust=False)["Adj Close"] #Adj pour obtenir prix après cloture -> prendre en compte les fractionnements + dividendes 
        if data.empty:
            raise ValueError("No data was downloaded, please verify tickers or time")
        
        data = data.dropna(how="all", axis=0)  # supprime les lignes vides
        data = data.dropna(how="all", axis=1)  # supprime les colonnes vides
        
        missing = [ticker for ticker in tickers if ticker not in data.columns]
        if missing:
            print(f"Data missing for : {missing}")
                
        if save_to_csv:
            filename = f"data_adj_{start}_{end}.csv"
            data.to_csv(filename)
            print(f"Data saved in {filename}")

        return data
    except Exception as e:
        print(f"Error while downloading data : {e}")
        return pd.DataFrame()


def get_benchmark(ticker="^GSPC", start=None, end=None) -> pd.Series:
    """
    Télécharge les prix ajustés du benchmark (ex: S&P500) via yfinance.

    Args:
        ticker (str): Ticker Yahoo Finance du benchmark (par défaut ^GSPC)
        start (str): Date de début au format 'YYYY-MM-DD'
        end (str): Date de fin au format 'YYYY-MM-DD'

    Returns:
        pd.Series: Série des prix ajustés du benchmark
    """
    try:
        data = yf.download(ticker, start=start, end=end, auto_adjust=True)
        benchmark = data["Close"].dropna()

        if benchmark.empty:
            raise ValueError("Aucune donnée téléchargée. Vérifiez le ticker ou la période.")

        return benchmark

    except Exception as e:
        print(f"Erreur lors du téléchargement du benchmark : {e}")
        return pd.Series()


import pandas as pd

def get_ff_factors(start, end, frequency='monthly'):
    """
    Télécharge et lit les facteurs Fama-French à partir des fichiers CSV (mensuel ou annuel).
    
    Args:
        start (str): Date de début au format 'YYYY-MM-DD'
        end (str): Date de fin au format 'YYYY-MM-DD'
        frequency (str): 'monthly' ou 'annual' pour spécifier la fréquence des données.
        
    Returns:
        factors (pd.DataFrame): DataFrame avec les facteurs MKT, SMB, HML
    """
    try:
        # Choisir le fichier CSV en fonction de la fréquence
        if frequency == 'monthly':
            factors = pd.read_csv('../data/FF_Data_Month.csv', header=None, names=["Date", "Mkt-RF", "SMB", "HML", "RF"])
        elif frequency == 'annual':
            factors = pd.read_csv('../data/FF_Data_Year.csv', header=None, names=["Date", "Mkt-RF", "SMB", "HML", "RF"])
        else:
            raise ValueError("La fréquence doit être 'monthly' ou 'annual'.")
        
        # Convertir la colonne 'Date' (au format YYYYMM) en format datetime (YYYY-MM-DD), avec le jour par défaut (01)
        factors['Date'] = pd.to_datetime(factors['Date'].astype(str) + '01', format='%Y%m%d')

        # Définir la colonne 'Date' comme index
        factors.set_index('Date', inplace=True)

        # Filtrer les données entre start et end
        factors = factors[(factors.index >= start) & (factors.index <= end)]

        # Convertir les valeurs en décimales (les facteurs sont donnés en pourcentages)
        factors[['Mkt-RF', 'SMB', 'HML']] = factors[['Mkt-RF', 'SMB', 'HML']] / 100

        # Renommer les colonnes pour correspondre à Fama-French
        factors = factors[['Mkt-RF', 'SMB', 'HML']]  # Garder seulement les facteurs
        factors.columns = ['MKT', 'SMB', 'HML']  # Renommer les colonnes

        return factors

    except Exception as e:
        print(f"Erreur lors du téléchargement des facteurs Fama-French : {e}")
        return pd.DataFrame()