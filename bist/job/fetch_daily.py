#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Günlük BIST verisi çekme işi.
Kullanım:
  python -m bist.job.fetch_daily
  python -m bist.job.fetch_daily --universe bist100
  python -m bist.job.fetch_daily --codes THYAO,GARAN,ASELS
"""

import argparse
import logging
import os
import sys
from datetime import datetime

import pandas as pd

# Proje kökünü path'e ekle
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from bist.core.stockfetch import fetch_stocks_spot, batch_fetch_hist
from bist.core.bist_symbols import get_default_symbols, normalize_code

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)


def main():
    parser = argparse.ArgumentParser(description="BIST günlük veri çekici")
    parser.add_argument("--universe", default="bist30", choices=["bist30", "bist100"],
                        help="Hisse evreni")
    parser.add_argument("--codes", default=None, help="Virgülle ayrılmış kodlar (THYAO,GARAN)")
    parser.add_argument("--period", default="1y", help="Geçmiş veri periyodu")
    parser.add_argument("--no-cache", action="store_true", help="Cache kullanma")
    args = parser.parse_args()

    if args.codes:
        symbols = [normalize_code(c.strip()) for c in args.codes.split(",") if c.strip()]
    else:
        symbols = get_default_symbols(args.universe)

    logger.info(f"{len(symbols)} hisse için veri çekiliyor ({args.universe})...")

    # Spot (son fiyatlar)
    spot = fetch_stocks_spot(symbols=symbols)
    if spot is not None and not spot.empty:
        out = os.path.join(DATA_DIR, f"spot_{datetime.now().strftime('%Y%m%d')}.csv")
        spot.to_csv(out, index=False)
        logger.info(f"Spot veri kaydedildi: {out} ({len(spot)} hisse)")
        print(spot[["code", "name", "close", "p_change", "volume"]].to_string(index=False))
    else:
        logger.warning("Spot veri alınamadı.")

    # Geçmiş OHLCV
    hist = batch_fetch_hist(
        symbols=symbols,
        period=args.period,
        use_cache=not args.no_cache,
    )
    logger.info(f"Geçmiş veri tamamlandı: {len(hist)} hisse")
    for code, df in list(hist.items())[:3]:
        logger.info(f"  {code}: {len(df)} gün, son kapanış={df['close'].iloc[-1]:.2f}")

    # Özet parquet (opsiyonel)
    if hist:
        summary_path = os.path.join(DATA_DIR, "hist_summary.csv")
        rows = []
        for code, df in hist.items():
            rows.append({
                "code": code,
                "days": len(df),
                "last_date": df["date"].iloc[-1],
                "last_close": df["close"].iloc[-1],
                "avg_volume": df["volume"].tail(20).mean(),
            })
        pd.DataFrame(rows).to_csv(summary_path, index=False)
        logger.info(f"Özet: {summary_path}")


if __name__ == "__main__":
    main()
