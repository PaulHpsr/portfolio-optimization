import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages


def plot_cumulative_returns(cumulative_df: pd.DataFrame, title: str = "Cumulative Returns"):
    plt.figure(figsize=(12, 6))
    cumulative_df.plot(ax=plt.gca())
    plt.title(title)
    plt.ylabel("Portfolio Value")
    plt.xlabel("Date")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_drawdown(cumulative: pd.Series, title: str = "Drawdown"):
    drawdown = cumulative / cumulative.cummax() - 1
    plt.figure(figsize=(12, 4))
    drawdown.plot(color='red')
    plt.title(title)
    plt.ylabel("Drawdown (%)")
    plt.xlabel("Date")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_efficient_frontier(returns_list: list, risks_list: list, sharpe_list: list):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=risks_list, y=returns_list, hue=sharpe_list, palette="viridis", s=100)
    plt.title("Efficient Frontier")
    plt.xlabel("Volatility")
    plt.ylabel("Expected Return")
    plt.colorbar(label="Sharpe Ratio")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def summary_table(returns: pd.Series) -> pd.DataFrame:
    cumulative = (1 + returns).cumprod()
    drawdown = cumulative / cumulative.cummax() - 1

    stats = {
        "Total Return": cumulative.iloc[-1] - 1,
        "Annualized Return": returns.mean() * 252,
        "Volatility": returns.std() * np.sqrt(252),
        "Sharpe Ratio": returns.mean() / returns.std() * np.sqrt(252),
        "Max Drawdown": drawdown.min()
    }

    return pd.DataFrame(stats, index=["Value"]).T


def export_report_pdf(filename: str, cumulative: pd.Series, drawdown: pd.Series, frontier_data: dict = None):
    """
    Exporte les graphiques de performance dans un fichier PDF
    
    Args:
        filename: nom du fichier PDF à créer
        cumulative: série des rendements cumulés
        drawdown: série des drawdowns
        frontier_data: dictionnaire avec 'returns', 'risks', 'sharpes' pour la frontière efficiente
    """
    with PdfPages(filename) as pdf:
        # Graphique des rendements cumulés
        plt.figure(figsize=(10, 5))
        cumulative.plot()
        plt.title("Rendements cumulés")
        plt.xlabel("Date")
        plt.ylabel("Valeur du portefeuille")
        plt.grid(True)
        pdf.savefig()
        plt.close()

        # Graphique des drawdowns
        plt.figure(figsize=(10, 4))
        drawdown.plot(color='red')
        plt.title("Drawdown")
        plt.xlabel("Date")
        plt.ylabel("Drawdown (%)")
        plt.grid(True)
        pdf.savefig()
        plt.close()

        # Graphique de la frontière efficiente (optionnel)
        if frontier_data:
            plt.figure(figsize=(8, 6))
            sns.scatterplot(
                x=frontier_data['risks'],
                y=frontier_data['returns'],
                hue=frontier_data['sharpes'],
                palette="viridis",
                s=100
            )
            plt.title("Frontière efficiente")
            plt.xlabel("Volatilité")
            plt.ylabel("Rendement attendu")
            plt.grid(True)
            pdf.savefig()
            plt.close()
