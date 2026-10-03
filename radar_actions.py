#!/usr/bin/env python3
"""
Radar actions : classe des actions selon un score momentum/tendance
pour un horizon de revente à 1 jour ou 7 jours.

Installation :  pip install yfinance pandas numpy
Utilisation  :  python radar_actions.py                 # classement du jour
                python radar_actions.py --backtest      # le score a-t-il marché dans le passé ?
                python radar_actions.py --tickers AAPL,TSLA,NVDA --top 3

Ce n'est PAS une prédiction : c'est un classement statistique. Lance --backtest
avant de te fier aux résultats, et vérifie que le titre est dispo sur Revolut.
"""
import argparse
import sys

import numpy as np
import pandas as pd
import yfinance as yf

# Actions US très liquides (en général disponibles sur Revolut). Modifie à ta guise.
UNIVERSE = (
    "AAPL MSFT NVDA AMZN GOOGL META TSLA AVGO AMD NFLX ADBE CRM ORCL INTC QCOM "
    "CSCO PYPL SHOP UBER ABNB COIN PLTR SNOW SQ DIS NKE SBUX MCD KO PEP WMT COST "
    "HD JPM BAC GS V MA XOM CVX PFE JNJ UNH LLY MRNA BA CAT GE F GM T VZ"
).split()


def load(tickers, period):
    data = yf.download(tickers, period=period, auto_adjust=True, progress=False)
    close = data["Close"].dropna(axis=1, how="all")
    volume = data["Volume"][close.columns]
    return close, volume


def rsi(close, n=14):
    delta = close.diff()
    up = delta.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    down = (-delta.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + up / down)


def zrow(df):
    z = df.sub(df.mean(axis=1), axis=0).div(df.std(axis=1), axis=0)
    return z.replace([np.inf, -np.inf], np.nan)


def compute(close, volume):
    ma20, ma50 = close.rolling(20).mean(), close.rolling(50).mean()
    return {
        "r5": close.pct_change(5),
        "r20": close.pct_change(20),
        "rsi": rsi(close),
        "volr": volume / volume.rolling(20).mean(),
        "trend": (close > ma20).astype(float) + (ma20 > ma50).astype(float),
        "vol": close.pct_change().abs().rolling(14).mean(),
    }


def score(f, horizon):
    if horizon == 1:
        # court terme : momentum 5j + volume anormal, en évitant le suracheté
        s = zrow(f["r5"]) + 0.5 * zrow(f["volr"]) - 0.5 * zrow((f["rsi"] - 55).abs())
    else:
        # 7 jours : tendance de fond + momentum 20j, RSI ni faible ni extrême
        s = zrow(f["r20"]) + zrow(f["trend"]) - 0.5 * zrow((f["rsi"] - 60).abs())
    return s.fillna(0)


def ranking(close, volume, horizon, top):
    f = compute(close, volume)
    s = score(f, horizon).iloc[-1]
    out = pd.DataFrame(
        {
            "score": s,
            "prix": close.iloc[-1],
            "5j %": f["r5"].iloc[-1] * 100,
            "20j %": f["r20"].iloc[-1] * 100,
            "RSI": f["rsi"].iloc[-1],
            "mvt/jour %": f["vol"].iloc[-1] * 100,
        }
    )
    return out.sort_values("score", ascending=False).head(top).round(2)


def backtest(close, volume, horizon, top):
    f = compute(close, volume)
    s = score(f, horizon)
    fwd = close.shift(-horizon) / close - 1
    mask = s.rank(axis=1, ascending=False) <= top
    picks = fwd.where(mask).mean(axis=1)
    base = fwd.mean(axis=1)
    d = pd.concat([picks, base], axis=1, keys=["picks", "base"]).dropna().iloc[60:]
    edge = d["picks"] - d["base"]
    print(f"  Jours testés            : {len(d)}")
    print(f"  Rendement moyen top {top}   : {d['picks'].mean() * 100:+.2f} %")
    print(f"  Rendement moyen univers : {d['base'].mean() * 100:+.2f} %")
    print(f"  Avantage moyen du score : {edge.mean() * 100:+.2f} % par trade")
    print(f"  Trades gagnants (top)   : {(d['picks'] > 0).mean() * 100:.0f} %")
    print(f"  Pire trade (top)        : {d['picks'].min() * 100:+.1f} %")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--tickers", help="liste séparée par des virgules")
    p.add_argument("--top", type=int, default=5)
    p.add_argument("--backtest", action="store_true")
    a = p.parse_args()

    tickers = [t.strip().upper() for t in a.tickers.split(",")] if a.tickers else UNIVERSE
    if len(tickers) < 5:
        sys.exit("Donne au moins 5 tickers (le score est relatif à l'univers).")

    close, volume = load(tickers, "2y" if a.backtest else "6mo")
    if a.backtest:
        for h in (1, 7):
            print(f"\n=== BACKTEST horizon {h} jour(s) (biais : univers = survivants actuels) ===")
            backtest(close, volume, h, a.top)
        print("\nSi l'avantage est ~0 ou négatif, le classement ne vaut pas mieux que le hasard.")
        return

    print(f"Données au {close.index[-1].date()} — {close.shape[1]} actions analysées")
    for h, label in ((1, "revente demain"), (7, "revente dans 7 jours")):
        print(f"\n=== Top {a.top} : {label} ===")
        print(ranking(close, volume, h, a.top).to_string())
    print(
        "\nClassement statistique, pas une prédiction. Les frais/spread Revolut et "
        "l'écart de prix à l'ouverture peuvent effacer un gain de 1 jour."
    )


if __name__ == "__main__":
    main()
