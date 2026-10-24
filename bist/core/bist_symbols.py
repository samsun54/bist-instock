#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BIST hisse listeleri.
yfinance ticker formatı: KOD.IS
Liste zaman zaman güncellenmelidir (hisse ekleme/çıkarma).
"""

# Popüler ve likit hisseler (BIST 30 + bazı BIST 100)
BIST30 = [
    "AKBNK.IS", "ARCLK.IS", "ASELS.IS", "ASTOR.IS", "BIMAS.IS",
    "EKGYO.IS", "ENKAI.IS", "EREGL.IS", "FROTO.IS", "GARAN.IS",
    "GUBRF.IS", "HEKTS.IS", "ISCTR.IS", "KCHOL.IS", "KONTR.IS",
    "KRDMD.IS", "ODAS.IS", "PETKM.IS", "PGSUS.IS", "SAHOL.IS",
    "SASA.IS", "SISE.IS", "TAVHL.IS", "TCELL.IS", "THYAO.IS",
    "TOASO.IS", "TUPRS.IS", "YKBNK.IS", "MGROS.IS", "ULKER.IS",
]

# Genişletilmiş BIST 100 benzeri liste (yfinance ile çalıştığı bilinenler)
BIST100 = BIST30 + [
    "AEFES.IS", "AGHOL.IS", "AKCNS.IS", "AKFGY.IS", "AKSEN.IS",
    "ALARK.IS", "ALBRK.IS", "ALGYO.IS", "ALKIM.IS", "ALTNY.IS",
    "ANELE.IS", "ANGEN.IS", "ARASE.IS", "ASUZU.IS", "AYDEM.IS",
    "BAGFS.IS", "BASGZ.IS", "BERA.IS", "BIENY.IS", "BIOEN.IS",
    "BRISA.IS", "BRYAT.IS", "BSOKE.IS", "BTCIM.IS", "BUCIM.IS",
    "CANTE.IS", "CCOLA.IS", "CEMTS.IS", "CIMSA.IS", "CWENE.IS",
    "DESA.IS", "DOAS.IS", "DOHOL.IS", "ECILC.IS", "EGEEN.IS",
    "ENERY.IS", "ENJSA.IS", "EUPWR.IS", "EUREN.IS", "FMIZP.IS",
    "GESAN.IS", "GLYHO.IS", "GOODY.IS", "GOZDE.IS", "GWIND.IS",
    "HALKB.IS", "HATSN.IS", "IPEKE.IS", "ISDMR.IS", "ISGYO.IS",
    "IZMDC.IS", "KAREL.IS", "KARSN.IS", "KARTN.IS", "KAYSE.IS",
    "KLRHO.IS", "KLSER.IS", "KMPUR.IS", "KONKA.IS", "KORDS.IS",
    "KRVGD.IS", "LOGO.IS", "MAVI.IS", "MGROS.IS", "MIATK.IS",
    "MPARK.IS", "NETAS.IS", "NTHOL.IS", "OTKAR.IS", "OYAKC.IS",
    "PARSN.IS", "PENTA.IS", "QUAGR.IS", "REEDR.IS", "RYGYO.IS",
    "SELEC.IS", "SKBNK.IS", "SMRTG.IS", "SNGYO.IS", "SOKM.IS",
    "TABGD.IS", "TATGD.IS", "TGSAS.IS", "TKFEN.IS", "TMSN.IS",
    "TRCAS.IS", "TSKB.IS", "TTKOM.IS", "TTRAK.IS", "ULKER.IS",
    "VAKBN.IS", "VESBE.IS", "VESTL.IS", "YEOTK.IS", "ZOREN.IS",
]

# Endeksler
INDICES = {
    "XU100.IS": "BIST 100",
    "XU030.IS": "BIST 30",
    "XBANK.IS": "BIST Banka",
    "XUSIN.IS": "BIST Sınai",
}


def get_default_symbols(universe: str = "bist30") -> list:
    """Varsayılan hisse listesini döner."""
    u = universe.lower()
    if u in ("bist30", "30"):
        return list(BIST30)
    if u in ("bist100", "100"):
        return list(BIST100)
    return list(BIST30)


def normalize_code(code: str) -> str:
    """Kodu yfinance formatına çevirir (THYAO -> THYAO.IS)."""
    code = code.strip().upper()
    if not code.endswith(".IS"):
        code = code + ".IS"
    return code


def display_code(code: str) -> str:
    """Görüntüleme için .IS uzantısını kaldırır."""
    return code.replace(".IS", "") if code.endswith(".IS") else code
