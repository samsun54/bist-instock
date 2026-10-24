#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tek hisse veya liste için indikatör hesaplama.
Kullanım:
  python -m bist.job.calc_indicators --code THYAO.IS
  python -m bist.job.calc_indicators --code GARAN --period 6mo
"""

import argparse
import logging
import os
import sys

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from bist.core.stockfetch import fetch_stock_hist
from bist.core.bist_symbols import normalize_code

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def _compute(df):
    try:
        import talib  # noqa: F401
        from bist.core.indicator.calculate_indicator import get_indicators
        return get_indicators(df)
    except ImportError:
        logger.warning("TA-Lib yüklü değil, basit (pandas) indikatörler kullanılıyor.")
        from bist.core.indicator.simple_indicators import add_basic_indicators
        return add_basic_indicators(df)
    except Exception as e:
        logger.warning(f"İndikatör hatası ({e}), basit indikatörlere geçiliyor.")
        from bist.core.indicator.simple_indicators import add_basic_indicators
        return add_basic_indicators(df)


def main():
    parser = argparse.ArgumentParser(description="BIST indikatör hesaplayıcı")
    parser.add_argument("--code", required=True, help="Hisse kodu (THYAO veya THYAO.IS)")
    parser.add_argument("--period", default="1y", help="Veri periyodu")
    parser.add_argument("--out", default=None, help="CSV çıktı yolu")
    args = parser.parse_args()

    code = normalize_code(args.code)
    logger.info(f"{code} verisi çekiliyor...")
    df = fetch_stock_hist(code, period=args.period)
    if df is None or df.empty:
        logger.error("Veri alınamadı.")
        sys.exit(1)

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    logger.info(f"{len(df)} satır ile indikatör hesaplanıyor...")
    result = _compute(df)
    if result is None or result.empty:
        logger.error("İndikatör hesaplanamadı.")
        sys.exit(1)

    cols_show = [c for c in ["date", "close", "macd", "macds", "macdh", "rsi",
                             "boll", "boll_ub", "boll_lb", "ma20", "ma60", "atr"]
                 if c in result.columns]
    print(result[cols_show].tail(8).to_string(index=False))

    out = args.out or os.path.join(ROOT, "data", f"indicators_{code.replace('.', '_')}.csv")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    result.to_csv(out, index=False)
    logger.info(f"Kaydedildi: {out}")


if __name__ == "__main__":
    main()
