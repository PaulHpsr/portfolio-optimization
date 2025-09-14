import numpy as np
import pandas as pd

def backtest_portfolio(weights: np.ndarray, returns: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule la performance historique d’un portefeuille à poids fixes.
    
    Args:
        weights: poids des actifs (np.ndarray)
        returns: rendements journaliers des actifs (pd.DataFrame)
    
    Returns:
        pd.DataFrame: rendements cumulés, volatilité, Sharpe, drawdown
    """
    portfolio_returns = returns @ weights
    cumulative_returns = (1 + portfolio_returns).cumprod()
    volatility = portfolio_returns.std() * np.sqrt(252)
    sharpe = portfolio_returns.mean() / portfolio_returns.std() * np.sqrt(252)
    drawdown = cumulative_returns / cumulative_returns.cummax() - 1

    return pd.DataFrame({
        'Cumulative': cumulative_returns,
        'Drawdown': drawdown,
        'Volatility': volatility,
        'Sharpe': sharpe
    })



def rolling_backtest(strategy_fn, returns: pd.DataFrame, window_size: int = 252, rebalance_freq: int = 21, transaction_fee: float = 1.0) -> pd.Series:
    """
    Backtest avec rééquilibrage périodique et frais de transaction fixes.
    
    Args:
        strategy_fn: fonction qui retourne les poids optimaux
        returns: rendements journaliers
        window_size: taille de la fenêtre d’estimation
        rebalance_freq: fréquence de rééquilibrage
        transaction_fee: coût fixe par actif modifié (1eur chez Trade Republic)
    
    Returns:
        pd.Series: rendements cumulés du portefeuille
    """
    dates = returns.index
    cumulative = []
    weights = None
    capital = 1.0  #capital initial
    prev_weights = np.zeros(returns.shape[1])

    for i in range(window_size, len(returns), rebalance_freq):
        window = returns.iloc[i - window_size:i]
        cov = window.cov().values
        mu = window.mean().values
        weights = strategy_fn(mu, cov)

        # Calcul des frais de transaction
        changed_positions = np.abs(weights - prev_weights) > 1e-4
        fee_total = transaction_fee * np.sum(changed_positions)
        capital -= fee_total / capital  #ajustement du capital

        # Application des rendements
        step_returns = returns.iloc[i:i + rebalance_freq] @ weights
        for r in step_returns:
            capital *= (1 + r)
            cumulative.append(capital)

        prev_weights = weights.copy()

    cumulative = pd.Series(cumulative, index=dates[window_size:window_size + len(cumulative)])
    return cumulative



def compare_strategies(strategy_dict: dict, returns: pd.DataFrame, window_size: int = 252, rebalance_freq: int = 21) -> pd.DataFrame:
    """
    Compare plusieurs stratégies de portefeuille
    
    Args:
        strategy_dict: dictionnaire {nom: fonction_stratégie}
        returns: rendements journaliers
        window_size: taille de la fenêtre
        rebalance_freq: fréquence de rééquilibrage
    
    Returns:
        pd.DataFrame: rendements cumulés par stratégie
    """
    results = {}
    for name, strategy_fn in strategy_dict.items():
        results[name] = rolling_backtest(strategy_fn, returns, window_size, rebalance_freq)

    return pd.DataFrame(results)
