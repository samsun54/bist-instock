#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BIST için uyarlanmış basit seçim stratejileri.
Orijinal Çin limit-up / 涨停 mantığı kaldırılmıştır.
"""

from typing import Optional
import pandas as pd
import numpy as np


def _prepare(data: pd.DataFrame, date=None, min_rows: int = 30) -> Optional[pd.DataFrame]:
    if data is None or data.empty:
        return None
    df = data.copy()
    if date is not None:
        end = date.strftime("%Y-%m-%d") if hasattr(date, "strftime") else str(date)
        df = df[df["date"].astype(str) <= end]
    if len(df) < min_rows:
        return None
    return df.sort_values("date").reset_index(drop=True)


def check_volume_up(data: pd.DataFrame, date=None, vol_ratio: float = 2.0, min_change: float = 1.0) -> bool:
    """
    Hacim artışı + yükseliş.
    - Son gün kapanış > açılış veya % değişim >= min_change
    - Son gün hacmi / 5 günlük ortalama hacim >= vol_ratio
    """
    df = _prepare(data, date, min_rows=10)
    if df is None:
        return False
    last = df.iloc[-1]
    avg_vol = df["volume"].tail(5).mean()
    if avg_vol <= 0:
        return False
    ratio = last["volume"] / avg_vol
    up = (last["close"] >= last["open"]) or (last.get("p_change", 0) >= min_change)
    return bool(up and ratio >= vol_ratio)


def check_ma_bullish(data: pd.DataFrame, date=None, ma_period: int = 30) -> bool:
    """
    MA yükselen trend (çoklu MA dizilimi basitleştirilmiş).
    - MA30 artıyor (10 gün önceye göre)
    - Fiyat MA30 üzerinde
    """
    df = _prepare(data, date, min_rows=ma_period + 15)
    if df is None:
        return False
    close = df["close"]
    ma = close.rolling(ma_period).mean()
    if ma.isna().iloc[-1]:
        return False
    # Son 10 günde MA yükseliyor mu?
    if ma.iloc[-1] <= ma.iloc[-11]:
        return False
    # Fiyat MA üzerinde
    return bool(close.iloc[-1] > ma.iloc[-1])


def check_turtle(data: pd.DataFrame, date=None, lookback: int = 20) -> bool:
    """
    Basit Turtle: son kapanış, son N günün en yükseği.
    """
    df = _prepare(data, date, min_rows=lookback + 1)
    if df is None:
        return False
    window = df["close"].iloc[-(lookback + 1):-1]
    last_close = df["close"].iloc[-1]
    return bool(last_close >= window.max())


def check_breakout_ma(data: pd.DataFrame, date=None, ma_period: int = 60) -> bool:
    """
    MA kırılımı: fiyat MA'yı yukarı kesiyor + hacim artışı.
    """
    df = _prepare(data, date, min_rows=ma_period + 5)
    if df is None:
        return False
    close = df["close"]
    ma = close.rolling(ma_period).mean()
    if ma.isna().iloc[-1] or ma.isna().iloc[-2]:
        return False
    # Dün altında veya eşit, bugün üstünde
    cross = close.iloc[-2] <= ma.iloc[-2] and close.iloc[-1] > ma.iloc[-1]
    if not cross:
        return False
    # Hacim en az 1.5x
    avg_vol = df["volume"].tail(5).mean()
    return bool(avg_vol > 0 and df["volume"].iloc[-1] >= 1.5 * avg_vol)


def run_all_strategies(data: pd.DataFrame, date=None) -> dict:
    """Tüm stratejileri çalıştırır, sonuç sözlüğü döner."""
    return {
        "hacim_artisi": check_volume_up(data, date),
        "ma_yukselis": check_ma_bullish(data, date),
        "turtle": check_turtle(data, date),
        "ma_kirilim": check_breakout_ma(data, date),
    }
