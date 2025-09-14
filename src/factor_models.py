import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression  #Pour estimer les betas

def run_capm(prices: pd.DataFrame, benchmark: pd.Series, risk_free_rate: float = 0.0) -> pd.Series:
    """
    Calcule les betas CAPM pour chaque actif par rapport au benchmark
    
    Args:
        prices (pd.DataFrame): Prix ajustés des actifs
        benchmark (pd.Series): Prix ajustés du marché
        risk_free_rate (float): Taux sans risque annuel
    
    Returns:
        pd.Series: Beta CAPM par actif
    """
    #Calcul des rendements
    returns = np.log(prices / prices.shift(1)).dropna()
    market_returns = np.log(benchmark / benchmark.shift(1)).dropna()
    #Convert. du taux sans risque en journalier
    rf_daily = risk_free_rate / 252
    excess_market = market_returns - rf_daily

    #Pour chaques actifs : 1)Calcul le rendement excédentaire 2)Regression linéaire (Ri-Rf = A +B(Rm-Rf))
    betas = {}
    for ticker in returns.columns:
        excess_asset = returns[ticker] - rf_daily
        model = LinearRegression().fit(excess_market.values.reshape(-1, 1), excess_asset.values)
        betas[ticker] = model.coef_[0]
    
    return pd.Series(betas)

def expected_returns_capm(betas: pd.Series, expected_market_return: float, risk_free_rate: float = 0.0) -> pd.Series:
    """
    Calcule les rendements attendus via le modèle CAPM.
    
    Args:
        betas (pd.Series): Sensibilité au marché.
        expected_market_return (float): Rendement attendu du marché.
        risk_free_rate (float): Taux sans risque.
    
    Returns:
        pd.Series: Rendements attendus par actif.
    """
    return risk_free_rate + betas * (expected_market_return - risk_free_rate)

#### Fama-French 3 Factors
    
# Ici statsmodels pour analyser la qualité du model + comparer avec CAPM
import statsmodels.api as sm
def run_fama_french_stats(returns: pd.DataFrame, factors: pd.DataFrame, risk_free_rate: float = 0.0) -> pd.DataFrame:
    """
    Estime les betas Fama-French 3 facteurs + alpha, R², p-values pour chaque actif
    
    Args:
        returns (pd.DataFrame): Rendements journaliers des actifs
        factors (pd.DataFrame): DataFrame avec les colonnes ['MKT', 'SMB', 'HML']
        risk_free_rate (float): Taux sans risque annuel
    
    Returns:
        pd.DataFrame: Résumé statistique par actif (alpha, betas, R², p-values)
    """
    rf_daily = risk_free_rate / 252  # Calcul du taux sans risque quotidien
    excess_factors = factors - rf_daily  # Ajustement des facteurs Fama-French
    results = []

    for ticker in returns.columns:
        try:
            # Rendement excédentaire de l'actif
            excess_returns = returns[ticker] - rf_daily
            X = sm.add_constant(excess_factors)  # Ajouter la constante (intercept)

            # Fusion des données pour filtrer les lignes valides
            df = pd.concat([excess_returns, X], axis=1).dropna()
            y = df.iloc[:, 0]  # Rendement excédentaire de l'actif
            X_clean = df.iloc[:, 1:]  # Facteurs Fama-French (incluant la constante)

            # Sécurité : ignorer si données vides
            if X_clean.empty or y.empty:
                print(f"Données insuffisantes pour {ticker}, régression ignorée.") 
                continue

            # Régression
            model = sm.OLS(y, X_clean).fit()

            # Collecter les résultats
            row = {
                'Alpha': model.params['const'] if 'const' in model.params else np.nan,
                'Beta_MKT': model.params.get('MKT', np.nan),
                'Beta_SMB': model.params.get('SMB', np.nan),
                'Beta_HML': model.params.get('HML', np.nan),
                'R_squared': model.rsquared,
                'p_MKT': model.pvalues.get('MKT', np.nan),
                'p_SMB': model.pvalues.get('SMB', np.nan),
                'p_HML': model.pvalues.get('HML', np.nan)
            }

            results.append(pd.Series(row, name=ticker))

        except Exception as e:
            print(f"Erreur pour {ticker} : {e}")

    return pd.DataFrame(results)

