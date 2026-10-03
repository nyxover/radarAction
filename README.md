pip install yfinance pandas numpy
python radar_actions.py              # top 5 du jour pour chaque horizon
python radar_actions.py --backtest   # teste le score sur 2 ans d'historique
python radar_actions.py --tickers AAPL,TSLA,NVDA,AMD,META --top 3


Exemple: 

$: python radar_actions.py              # top 5 du jour pour chaque horizon
$SQ: No data found, symbol may be delisted

1 Failed download:
['SQ']: No data found, symbol may be delisted
Données au 2026-10-02 — 51 actions analysées

=== Top 5 : revente demain ===
        score    prix  5j %  20j %    RSI  mvt/jour %
Ticker
CSCO     2.81  112.20  5.56   3.71  58.16        1.26
SHOP     2.41  151.39  6.43   3.78  61.14        2.33
NVDA     2.36  233.95  3.95   2.52  63.01        1.12
ORCL     2.08  142.30  3.79  -7.62  48.31        2.34
CAT      2.03  845.42  2.90   5.66  58.84        1.14

=== Top 5 : revente dans 7 jours ===
        score    prix  5j %  20j %    RSI  mvt/jour %
Ticker
AMD      5.54  633.91  0.52  38.97  70.07        2.59
INTC     5.21  119.33 -2.98  30.17  60.64        3.17
MRNA     4.72  190.01 -4.46  27.63  66.22        3.80
META     4.21  728.08 -3.14  19.32  61.54        2.58
PLTR     2.82  188.75 -0.49   3.41  61.18        1.20

Classement statistique, pas une prédiction. Les frais/spread Revolut et l'écart de prix à l'ouverture peuvent effacer un gain de 1 jour.
