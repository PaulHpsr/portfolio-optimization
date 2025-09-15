
# Portfolio Optimization - CAPM & Fama-French

## Description
Ce projet propose un pipeline modulaire et reproductible pour concevoir, simuler et évaluer un portefeuille d’actifs inspiré du S&P 500. Il inclut le chargement des données, l’estimation des rendements et de la covariance, l’optimisation moyenne-variance (Markowitz) et Sharpe, le backtesting avec rééquilibrage et frais de transaction, la comparaison de stratégies, et la génération automatisée de rapports graphiques et PDF.

## Fonctionnalités
# Portfolio Optimization – CAPM & Fama-French

## Description

Ce projet propose un pipeline modulaire et reproductible pour concevoir, simuler et évaluer un portefeuille d’actifs inspiré du S&P 500. Il combine :

- Estimation des rendements attendus via les modèles **CAPM** et **Fama-French**
- Optimisation moyenne-variance (Markowitz) et maximisation du ratio de Sharpe
- Backtesting avec rééquilibrage périodique et frais de transaction
- Benchmarking contre le S&P 500
- Reporting automatisé (graphique + PDF)

---

## Fonctionnalités

- Chargement des prix ajustés (Yahoo Finance via `get_data_adj`) et calcul des rendements log  
- Estimation des paramètres  
  - Rendements attendus (`mu`) : CAPM & Fama-French  
  - Matrice de covariance (`cov`)  
- Optimisation moyenne-variance  
  - Portefeuille à variance minimale  
  - Maximisation du ratio de Sharpe  
  - Objectif personnalisé et bornes sur les poids  
- Backtesting  
  - `backtest_portfolio()`: simulation à poids fixes  
  - `rolling_backtest()`: rééquilibrage périodique + frais  
  - `compare_strategies()`: comparaison de plusieurs approches  
- Benchmarking  
  - Performance cumulée vs S&P 500  
  - Calcul de l’alpha et du tracking error  
- Reporting  
  - Graphiques : rendements cumulés, drawdown, frontière efficiente  
  - Tableau de synthèse : rendement annualisé, volatilité, Sharpe, max drawdown  
  - Export PDF automatique (`export_report_pdf()`) 

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
    - Rendement cumulatif et drawdown
    - Volatilité annualisée et ratio de Sharpe
    - Comparaison avec le benchmark S&P 500

## Auteur
**Paul HOPSORE**  
[LinkedIn](https://www.linkedin.com/in/paul-hopsore-19576732a/)
