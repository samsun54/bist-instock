#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BIST-InStock — Tek dosyadan kurulum kontrolü + örnek çalıştırma
Kullanım:
  python kurulum_ve_calistir.py
"""

import subprocess
import sys


def pip_install(packages):
    print("Eksik paketler yükleniyor:", ", ".join(packages))
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q"] + packages)


def check_and_install():
    need = []
    for pkg, import_name in [
        ("yfinance", "yfinance"),
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("tqdm", "tqdm"),
        ("requests", "requests"),
    ]:
        try:
            __import__(import_name)
        except ImportError:
            need.append(pkg)
    if need:
        pip_install(need)
    print("OK — gerekli paketler hazır.\n")


def demo():
    import yfinance as yf
    import pandas as pd

    print("=" * 50)
    print("BIST örnek veri (THYAO.IS + GARAN.IS)")
    print("=" * 50)

    for code in ["THYAO.IS", "GARAN.IS"]:
        t = yf.Ticker(code)
        hist = t.history(period="5d", auto_adjust=False)
        if hist.empty:
            print(f"{code}: veri yok")
            continue
        last = hist.iloc[-1]
        prev = hist.iloc[-2] if len(hist) > 1 else last
        chg = (last["Close"] - prev["Close"]) / prev["Close"] * 100
        print(f"{code:12}  Kapanış: {last['Close']:.2f}  "
              f"Değişim: %{chg:+.2f}  Hacim: {int(last['Volume']):,}")

    print("\nSon 5 gün THYAO:")
    thyao = yf.Ticker("THYAO.IS").history(period="1mo", auto_adjust=False)
    if not thyao.empty:
        print(thyao[["Open", "High", "Low", "Close", "Volume"]].tail(5).to_string())

    print("\n" + "=" * 50)
    print("Çalışıyor! Sonraki adımlar:")
    print("  python -m bist.job.fetch_daily --codes THYAO,GARAN,ASELS")
    print("  python -m bist.job.calc_indicators --code THYAO")
    print("  python -m bist.job.run_strategies")
    print("=" * 50)


if __name__ == "__main__":
    print("BIST-InStock kurulum kontrolü...\n")
    try:
        check_and_install()
        demo()
    except Exception as e:
        print("\nHATA:", e)
        print("\nManuel kurulum:")
        print("  pip install yfinance pandas numpy tqdm requests")
        print("  python kurulum_ve_calistir.py")
        sys.exit(1)
