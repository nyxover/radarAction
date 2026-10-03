

python radar_actions.py --backtest # teste le score sur 2 ans d'historique

python radar_actions.py --tickers AAPL,TSLA,NVDA,AMD,META --top 3

python radar_actions.py --backtest
 
 
 python radar_actions.py              # top 5 du jour pour chaque horizon
Données au 2026-10-02 — 52 actions analysées

=== Top 5 : revente demain ===
        score    prix  5j %  20j %    RSI  mvt/jour %
Ticker
CSCO     2.85  112.20  5.56   3.71  58.16        1.26
SHOP     2.44  151.39  6.43   3.78  61.14        2.33
NVDA     2.39  233.95  3.95   2.52  63.01        1.12
ORCL     2.11  142.30  3.79  -7.62  48.31        2.34
CAT      2.05  845.42  2.90   5.66  58.84        1.14

=== Top 5 : revente dans 7 jours ===
        score    prix  5j %  20j %    RSI  mvt/jour %
Ticker
AMD      5.60  633.91  0.52  38.97  70.07        2.59
INTC     5.27  119.33 -2.98  30.17  60.64        3.17
MRNA     4.78  190.01 -4.46  27.63  66.22        3.80
META     4.26  728.08 -3.14  19.32  61.54        2.58
PLTR     2.87  188.75 -0.49   3.41  61.18        1.20

Classement statistique, pas une prédiction. Les frais/spread Revolut et l'écart de prix à l'ouverture peuvent effacer un gain de 1 jour.

Lecture de tes résultats :

Revente demain (CSCO, SHOP, NVDA, ORCL, CAT) : ce classement récompense surtout les titres qui ont monté ces 5 derniers jours avec du volume. Sur 1 jour, ce genre de signal est faible, et le gain moyen attendu est souvent du même ordre que les frais et l'écart de prix à l'ouverture.
Revente dans 7 jours (AMD, INTC, MRNA, META, PLTR) : ce sont les titres qui ont le plus monté sur 20 jours (+39 % pour AMD, +30 % pour INTC, +28 % pour MRNA). Acheter après une telle hausse, c'est parier que la tendance continue. Le risque inverse existe : AMD est déjà à un RSI de 70, et un repli de 5 à 10 % en une semaine y serait banal. MRNA et INTC bougent en moyenne de plus de 3 % par jour, donc la perte possible est aussi large que le gain.

Avant de mettre de l'argent dessus, lance python radar_actions.py --backtest. Il te dira si ce classement a déjà fait mieux que la moyenne des 52 actions sur 2 ans. Si l'avantage est proche de zéro, le classement n'est pas meilleur que le hasard, et tu le sauras avant d'avoir risqué quoi que ce soit.
