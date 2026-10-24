#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Borsa İstanbul veri çekme katmanı (yfinance tabanlı).
Orijinal InStock'un East Money bağımlılığı kaldırılmıştır.
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Optional, List, Dict

import pandas as pd
import yfinance as yf
from tqdm import tqdm

from bist.core.bist_symbols import (
    get_default_symbols, normalize_code, display_code, INDICES
)

logger = logging.getLogger(__name__)

# Cache dizini
_CACHE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "cache", "hist"
)
os.makedirs(_CACHE_DIR, exist_ok=True)


def _to_ohlcv(df: pd.DataFrame, code: str) -> pd.DataFrame:
    """yfinance DataFrame'ini standart OHLCV formatına çevirir."""
    if df is None or df.empty:
        return pd.DataFrame()

    df = df.copy()
    df = df.rename(columns={
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume",
        "Adj Close": "adj_close",
    })
    df.index = pd.to_datetime(df.index)
    df = df.reset_index()
    # Kolon adı bazen Date, bazen Datetime olabilir
    date_col = "Date" if "Date" in df.columns else "Datetime"
    if date_col in df.columns:
        df = df.rename(columns={date_col: "date"})
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df["code"] = code
    df["name"] = display_code(code)

    # Yüzde değişim
    df["p_change"] = df["close"].pct_change() * 100

    cols = ["date", "code", "name", "open", "high", "low", "close", "volume", "p_change"]
    if "adj_close" in df.columns:
        cols.append("adj_close")
    return df[[c for c in cols if c in df.columns]].dropna(subset=["close"])


def fetch_stock_hist(
    code: str,
    start: Optional[str] = None,
    end: Optional[str] = None,
    period: str = "1y",
    use_cache: bool = True,
) -> Optional[pd.DataFrame]:
    """
    Tek hisse geçmiş verisi.
    :param code: THYAO veya THYAO.IS
    :param start: YYYY-MM-DD
    :param end: YYYY-MM-DD
    :param period: yfinance period (1mo, 3mo, 6mo, 1y, 2y, 5y, max)
    """
    code = normalize_code(code)
    cache_file = os.path.join(_CACHE_DIR, f"{code.replace('.', '_')}.csv")

    try:
        if use_cache and os.path.exists(cache_file):
            mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if (datetime.now() - mtime) < timedelta(hours=6):
                df = pd.read_csv(cache_file, parse_dates=["date"])
                df["date"] = pd.to_datetime(df["date"]).dt.date
                return df

        ticker = yf.Ticker(code)
        if start or end:
            df = ticker.history(start=start, end=end, auto_adjust=False)
        else:
            df = ticker.history(period=period, auto_adjust=False)

        result = _to_ohlcv(df, code)
        if not result.empty and use_cache:
            result.to_csv(cache_file, index=False)
        return result if not result.empty else None

    except Exception as e:
        logger.error(f"fetch_stock_hist {code} hata: {e}")
        return None


def fetch_stocks_spot(
    symbols: Optional[List[str]] = None,
    universe: str = "bist30",
) -> Optional[pd.DataFrame]:
    """
    Birden fazla hissenin son fiyat bilgisini çeker.
    """
    if symbols is None:
        symbols = get_default_symbols(universe)
    symbols = [normalize_code(s) for s in symbols]

    rows = []
    for code in tqdm(symbols, desc="Spot veri çekiliyor"):
        try:
            t = yf.Ticker(code)
            info = t.fast_info
            hist = t.history(period="5d", auto_adjust=False)
            if hist.empty:
                continue
            last = hist.iloc[-1]
            prev = hist.iloc[-2] if len(hist) > 1 else last
            change = (last["Close"] - prev["Close"]) / prev["Close"] * 100 if prev["Close"] else 0

            rows.append({
                "code": code,
                "name": display_code(code),
                "open": float(last["Open"]),
                "high": float(last["High"]),
                "low": float(last["Low"]),
                "close": float(last["Close"]),
                "volume": float(last["Volume"]),
                "p_change": round(change, 2),
                "date": last.name.date() if hasattr(last.name, "date") else datetime.now().date(),
            })
        except Exception as e:
            logger.debug(f"Spot {code} atlandı: {e}")
            continue

    if not rows:
        return None
    return pd.DataFrame(rows)


def fetch_index_hist(index_code: str = "XU100.IS", period: str = "1y") -> Optional[pd.DataFrame]:
    """Endeks geçmiş verisi (XU100.IS, XU030.IS ...)."""
    return fetch_stock_hist(index_code, period=period)


def batch_fetch_hist(
    symbols: Optional[List[str]] = None,
    universe: str = "bist30",
    period: str = "1y",
    use_cache: bool = True,
) -> Dict[str, pd.DataFrame]:
    """Birden fazla hisse için geçmiş veri sözlüğü döner."""
    if symbols is None:
        symbols = get_default_symbols(universe)
    result = {}
    for code in tqdm(symbols, desc="Geçmiş veri"):
        df = fetch_stock_hist(code, period=period, use_cache=use_cache)
        if df is not None and not df.empty:
            result[normalize_code(code)] = df
    return result
