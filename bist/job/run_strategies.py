#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Strateji taraması — BIST hisselerinde.
Kullanım:
  python -m bist.job.run_strategies
  python -m bist.job.run_strategies --universe bist100
"""

import argparse
import logging
import os
import sys
from datetime import datetime

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from bist.core.stockfetch import batch_fetch_hist
from bist.core.bist_symbols import get_default_symbols, display_code
from bist.core.strategy import run_all_strategies

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)


def main():
    parser = argparse.ArgumentParser(description="BIST strateji tarayıcı")
    parser.add_argument("--universe", default="bist30", choices=["bist30", "bist100"])
    parser.add_argument("--period", default="6mo")
    args = parser.parse_args()

    symbols = get_default_symbols(args.universe)
    logger.info(f"{len(symbols)} hisse taranıyor...")

    hist = batch_fetch_hist(symbols=symbols, period=args.period, use_cache=True)
    results = []

    for code, df in hist.items():
        try:
            signals = run_all_strategies(df)
            if any(signals.values()):
                last = df.iloc[-1]
                results.append({
                    "code": display_code(code),
                    "close": round(float(last["close"]), 2),
                    "p_change": round(float(last.get("p_change", 0) or 0), 2),
                    **signals,
                })
        except Exception as e:
            logger.debug(f"{code} strateji hatası: {e}")

    if not results:
        logger.info("Hiçbir hisse strateji sinyali vermedi.")
        return

    df_out = pd.DataFrame(results)
    # En az bir True olanları öne al
    df_out["score"] = df_out[["hacim_artisi", "ma_yukselis", "turtle", "ma_kirilim"]].sum(axis=1)
    df_out = df_out.sort_values("score", ascending=False)

    print("\n=== Strateji Sonuçları ===\n")
    print(df_out.to_string(index=False))

    out = os.path.join(DATA_DIR, f"strategies_{datetime.now().strftime('%Y%m%d_%H%M')}.csv")
    df_out.to_csv(out, index=False)
    logger.info(f"Kaydedildi: {out}")


if __name__ == "__main__":
    main()
