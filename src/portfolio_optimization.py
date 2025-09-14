import numpy as np
import pandas as pd
from scipy.optimize import minimize #Optimisation numérique

def mean_variance_optimization(expected_returns: np.ndarray, cov_matrix: np.ndarray, target_return: float) -> np.ndarray:
    """
    Minimise la variance pour un rendement cible, trouver les poids tout en atteignant le rendement ciblé
    """
    n = len(expected_returns) #Nbr actifs

    #Fonction objectif
    def portfolio_variance(weights):   
        return weights.T @ cov_matrix @ weights   

    #Somme des poids = 1
    constraints = [
        {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
        {'type': 'eq', 'fun': lambda w: w @ expected_returns - target_return}
    ]
    
    bounds = [(0, 1) for _ in range(n)] #Pas de vente à découvert
    init_guess = np.ones(n) / n #Portfeuille égalitaire

    result = minimize(portfolio_variance, init_guess, bounds=bounds, constraints=constraints)
    return result.x


def max_sharpe_portfolio(expected_returns: np.ndarray, cov_matrix: np.ndarray, risk_free_rate: float = 0.0) -> np.ndarray:
    """
    Maximisation du ratio de Sharpe
    """
    n = len(expected_returns)

    #Negatif du sharp -> car on cherche à minimiser (minimize)
    def neg_sharpe(weights):
        port_return = weights @ expected_returns
        port_vol = np.sqrt(weights.T @ cov_matrix @ weights)
        return - (port_return - risk_free_rate) / port_vol

    constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
    bounds = [(0, 1) for _ in range(n)]
    init_guess = np.ones(n) / n

    result = minimize(neg_sharpe, init_guess, bounds=bounds, constraints=constraints)
    return result.x



def min_variance_portfolio(cov_matrix: np.ndarray) -> np.ndarray:
    """
    Portefeuille à volatilité minimale
    """
    n = cov_matrix.shape[0]

    def portfolio_volatility(weights):
        return np.sqrt(weights.T @ cov_matrix @ weights)

    constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
    bounds = [(0, 1) for _ in range(n)]
    init_guess = np.ones(n) / n

    result = minimize(portfolio_volatility, init_guess, bounds=bounds, constraints=constraints)
    return result.x



def custom_objective_portfolio(objective_fn, expected_returns: np.ndarray, cov_matrix: np.ndarray, constraints=None, bounds=None) -> np.ndarray:
    """
    Optimisation avec objectif personnalisé
    
    Args:
        objective_fn: fonction à minimiser 
        ( lambda w: -w @ expected_returns -> maximiser le rendement.
        lambda w: w.T @ cov_matrix @ w -> minimiser la variance.
        lambda w: -custom_alpha(w) -> maximiser un alpha calculé.)
        
        expected_returns: rendements attendus
        cov_matrix: matrice de covariance
        constraints: contraintes supplémentaires
        bounds: bornes sur les poids
    
    Returns:
        np.ndarray: poids optimaux
    """
    n = len(expected_returns)
    if bounds is None:
        bounds = [(0, 1) for _ in range(n)]
    if constraints is None:
        constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
    init_guess = np.ones(n) / n

    result = minimize(objective_fn, init_guess, bounds=bounds, constraints=constraints)
    return result.x
