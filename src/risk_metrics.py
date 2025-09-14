import numpy as np
import pandas as pd

def compute_returns(prices:pd.DataFrame, log:bool = True):
    """
    Calcule les rendements à partir des prix.
    
    Args:
        prices (pd.DataFrame): Prix ajustés.
        log (bool): Si True, rendements logarithmiques. Sinon, rendements simples.
    
    Returns:
        pd.DataFrame: Rendements journaliers.
    """
    if log:
        return np.log(prices / prices.shift(1)).dropna() #Rendements logarithmiques
    else:
        return prices.pct_change().dropna()  #Rendements simple
    
def compute_volatility(returns: pd.DataFrame) -> pd.Series:
    """
    Calcule la volatilité journalière (écart type)
    
    Args:
        returns (pd.DataFrame): Rendements journaliers
    
    Returns:
        pd.Series: Volatilité par actif
    """
    return returns.std() #Ecart type

def compute_sharpe_ratio(returns: pd.DataFrame, risk_free_rate: float = 0.0) -> pd.Series:
    """
    Calcule le Sharpe Ratio annualisé
    
    Args:
        returns (pd.DataFrame): Rendements journaliers
        risk_free_rate (float): Taux sans risque annuel
    
    Returns:
        pd.Series: Sharpe Ratio par actif
    """
    rf_daily = risk_free_rate / 252 #Taux sans risque annuel -> Journalier (252 jours de bourse / ans)
    excess_return = returns - rf_daily  #Rendement au dessus du taux sans risque pour chaques actifs
    sharpe = excess_return.mean() / excess_return.std()
    return sharpe * np.sqrt(252)  #Annualisation du sharpe ratio