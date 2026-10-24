#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TA-Lib olmadan çalışan temel indikatörler (pandas).
Tam sürüm için TA-Lib + calculate_indicator.py kullanın.
"""

import pandas as pd
import numpy as np


def add_basic_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """OHLCV DataFrame'e temel indikatör kolonları ekler."""
    data = df.copy()
    c = data["close"]
    h = data["high"]
    l = data["low"]

    # Hareketli ortalamalar
    data["ma5"] = c.rolling(5).mean()
    data["ma10"] = c.rolling(10).mean()
    data["ma20"] = c.rolling(20).mean()
    data["ma60"] = c.rolling(60).mean()

    # RSI (14)
    delta = c.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    data["rsi"] = 100 - (100 / (1 + rs))

    # MACD
    ema12 = c.ewm(span=12, adjust=False).mean()
    ema26 = c.ewm(span=26, adjust=False).mean()
    data["macd"] = ema12 - ema26
    data["macds"] = data["macd"].ewm(span=9, adjust=False).mean()
    data["macdh"] = data["macd"] - data["macds"]

    # Bollinger
    mid = c.rolling(20).mean()
    std = c.rolling(20).std()
    data["boll"] = mid
    data["boll_ub"] = mid + 2 * std
    data["boll_lb"] = mid - 2 * std

    # ATR (14)
    tr = pd.concat([
        h - l,
        (h - c.shift()).abs(),
        (l - c.shift()).abs(),
    ], axis=1).max(axis=1)
    data["atr"] = tr.rolling(14).mean()

    return data
