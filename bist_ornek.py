#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BIST basit örnek — paket yapısına gerek yok.
Sadece:  pip install yfinance pandas
Sonra:   python bist_ornek.py
"""

import sys

try:
    import yfinance as yf
    import pandas as pd
except ImportError:
    print("Önce şunu çalıştır:")
    print("  pip install yfinance pandas")
    sys.exit(1)


HISSALER = ["THYAO.IS", "GARAN.IS", "ASELS.IS", "TUPRS.IS", "BIMAS.IS", "EREGL.IS"]


def main():
    print("Borsa İstanbul — son fiyatlar\n")
    rows = []
    for code in HISSALER:
        try:
            t = yf.Ticker(code)
            h = t.history(period="5d", auto_adjust=False)
            if h.empty:
                print(f"  {code}: veri yok (ticker hatalı olabilir)")
                continue
            last = h.iloc[-1]
            prev = h.iloc[-2] if len(h) > 1 else last
            chg = (last["Close"] - prev["Close"]) / prev["Close"] * 100 if prev["Close"] else 0
            rows.append({
                "Kod": code.replace(".IS", ""),
                "Kapanış": round(float(last["Close"]), 2),
                "Değişim %": round(chg, 2),
                "Hacim": int(last["Volume"]),
            })
        except Exception as e:
            print(f"  {code}: hata — {e}")

    if rows:
        df = pd.DataFrame(rows)
        print(df.to_string(index=False))
        print("\nBaşarılı. Sistem çalışıyor.")
    else:
        print("Hiç veri alınamadı. İnternet bağlantını kontrol et.")


if __name__ == "__main__":
    main()
