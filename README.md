
# Portfolio Optimization - CAPM & Fama-French

## Description
Ce projet propose un pipeline modulaire et reproductible pour concevoir, simuler et évaluer un portefeuille d’actifs inspiré du S&P 500. Il inclut le chargement des données, l’estimation des rendements et de la covariance, l’optimisation moyenne-variance (Markowitz) et Sharpe, le backtesting avec rééquilibrage et frais de transaction, la comparaison de stratégies, et la génération automatisée de rapports graphiques et PDF.

## Fonctionnalités
- Chargement des prix ajustés (Yahoo Finance via get_data_adj) et calcul des rendements log
- Estimation des paramètres : rendements attendus (mu), covariance (cov)
- Optimisation moyenne-variance :
    Portefeuille à variance minimale
    Maximisation du ratio de Sharpe
    Objectif personnalisé et bornes sur les poids
- Backtesting :
    backtest_portfolio() pour simulation à poids fixes
    rolling_backtest() pour rééquilibrage périodique et prise en compte des frais
    compare_strategies() pour comparer plusieurs approches
- Benchmarking contre le S&P 500 : comparaison de la performance cumulée, calcul de l’alpha et du tracking error
- Reporting :
    Graphiques des rendements cumulés, drawdown et frontière efficiente
    Tableau de synthèse (rendement annualisé, volatilité, Sharpe, max drawdown)
    Export PDF automatisé via export_report_pdf()  

## Structure du projet
- `src/` : fichiers source Python (`data_loader.py`, `risk_metrics.py`, `factors_models.py`, `backtesting.py`, `portfolio_optimization.py` `reporting.py`)  
- `notebooks/` : notebooks pour exploration, analyse, visualisation  
- `README.md` : ce fichier  
- `requirements.txt` : liste des dépendances Python  

## Installation
Cloner le repo :  
```bash
git clone [https://github.com/PaulHpsr/portfolio-optimization](https://github.com/PaulHpsr/portfolio-optimization)
cd portfolio-project
```

Installer les dépendances :  
```bash
pip install -r requirements.txt
```

## Utilisation
- Modifier la liste des tickers et la période dans les notebooks Jupyter.  
- Exécuter notebooks/portfolio_backtesting.ipynb pour générer les poids optimaux et lancer le backtest (avec rééquilibrage et frais). 
- Exécuter notebooks/portfolio_reporting.ipynb pour visualiser les performances, le drawdown, la frontière efficiente, et exporter le rapport PDF. 
- Pour comparer plusieurs stratégies, adapter le dictionnaire strategy_dict dans backtesting.py et relancer le backtest.  

## Résultats
Le pipeline fournit une évaluation détaillée de chaque stratégie :
    Rendement cumulatif et drawdown
    Volatilité annualisée et ratio de Sharpe
    Comparaison avec le benchmark S&P 500

## Auteur
**Paul HOPSORE**  
[LinkedIn](https://www.linkedin.com/in/paul-hopsore-19576732a/)
