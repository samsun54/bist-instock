#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Borsa İstanbul seans saatleri ve işlem günü kontrolü.
Türkiye saati (Europe/Istanbul) varsayılır.
"""

import datetime
from typing import Optional, Set

# Basit resmi tatil listesi (her yıl güncellenmeli)
# Format: (ay, gün) — sabit tarihler. Değişken tatiller (Ramazan, Kurban) için genişletilebilir.
FIXED_HOLIDAYS = {
    (1, 1),   # Yılbaşı
    (4, 23),  # Ulusal Egemenlik ve Çocuk Bayramı
    (5, 1),   # Emek ve Dayanışma Günü
    (5, 19),  # Atatürk'ü Anma, Gençlik ve Spor Bayramı
    (7, 15),  # Demokrasi ve Milli Birlik Günü
    (8, 30),  # Zafer Bayramı
    (10, 29), # Cumhuriyet Bayramı
}

# Seans saatleri (BIST sürekli seans)
OPEN_TIME = (
    (datetime.time(10, 0, 0), datetime.time(18, 0, 0)),
)


def is_weekend(date: datetime.date) -> bool:
    return date.weekday() >= 5  # Cumartesi=5, Pazar=6


def is_fixed_holiday(date: datetime.date) -> bool:
    return (date.month, date.day) in FIXED_HOLIDAYS


def is_trade_date(date: Optional[datetime.date] = None,
                  extra_holidays: Optional[Set[datetime.date]] = None) -> bool:
    """Verilen tarihin BIST işlem günü olup olmadığını kontrol eder."""
    if date is None:
        date = datetime.date.today()
    if is_weekend(date) or is_fixed_holiday(date):
        return False
    if extra_holidays and date in extra_holidays:
        return False
    return True


def get_previous_trade_date(date: datetime.date, count: int = 1) -> datetime.date:
    """Önceki işlem gününü bulur."""
    tmp = date
    while count > 0:
        tmp -= datetime.timedelta(days=1)
        if is_trade_date(tmp):
            count -= 1
    return tmp


def get_next_trade_date(date: datetime.date) -> datetime.date:
    """Sonraki işlem gününü bulur."""
    tmp = date
    while True:
        tmp += datetime.timedelta(days=1)
        if is_trade_date(tmp):
            return tmp


def is_tradetime(now_time: Optional[datetime.datetime] = None) -> bool:
    """Şu an seans içinde mi?"""
    if now_time is None:
        now_time = datetime.datetime.now()
    if not is_trade_date(now_time.date()):
        return False
    now = now_time.time()
    for begin, end in OPEN_TIME:
        if begin <= now < end:
            return True
    return False


def is_close(now_time: Optional[datetime.datetime] = None) -> bool:
    """Seans kapandı mı?"""
    if now_time is None:
        now_time = datetime.datetime.now()
    return now_time.time() >= datetime.time(18, 0, 0)
