# BIST-InStock — Borsa İstanbul Hisse Analiz Sistemi

Çin InStock projesinden uyarlanmış, **Borsa İstanbul (BIST)** için yeniden düzenlenmiş hisse senedi analiz ve seçim sistemi.

## Özellikler

- **BIST 100 / BIST 30** hisse listesi
- Günlük OHLCV verisi (`yfinance` ile `.IS` ticker'ları)
- Teknik indikatörler (MACD, KDJ, BOLL, RSI, ATR, Supertrend vb. — TA-Lib)
- Basit strateji motoru (hacim artışı, MA kesişimi, turtle vb.)
- Türkiye seans saatleri ve tatil kontrolü
- Türkçe arayüz metinleri ve loglar
- CLI ile günlük veri çekme + indikatör hesaplama

## Kurulum

```bash
# Python 3.10+ önerilir
cd bist-instock
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

# TA-Lib sistem kütüphanesi gerekir (Ubuntu/Debian):
# sudo apt-get install -y build-essential libta-lib0 libta-lib0-dev
# veya conda: conda install -c conda-forge ta-lib
```

## Hızlı Başlangıç

```bash
# BIST 100 listesini ve son verileri çek
python -m bist.job.fetch_daily

# Belirli bir hisse için indikatör hesapla
python -m bist.job.calc_indicators --code THYAO.IS

# Strateji taraması (örnek: hacim artışı + MA yükseliş)
python -m bist.job.run_strategies
```

## Dizin Yapısı

```
bist-instock/
├── bist/
│   ├── core/
│   │   ├── crawling/          # Veri çekme (yfinance tabanlı)
│   │   ├── indicator/         # Teknik indikatör hesaplama
│   │   ├── strategy/          # Seçim stratejileri
│   │   └── stockfetch.py      # Ana veri arayüzü
│   ├── job/                   # Günlük işler
│   ├── lib/                   # Yardımcı (seans saati, takvim)
│   └── web/                   # (İsteğe bağlı) basit web arayüzü
├── data/                      # CSV / parquet çıktılar
├── cache/                     # Geçici cache
├── requirements.txt
└── README.md
```

## Veri Kaynağı

Ücretsiz ve stabil kaynak olarak **yfinance** kullanılır:

- Ticker formatı: `THYAO.IS`, `GARAN.IS`, `ASELS.IS` ...
- BIST 100 listesi kod içinde güncellenebilir veya KAP / BIST sitesinden alınabilir.

Not: yfinance gecikmeli veya eksik veri verebilir. Profesyonel kullanım için ücretli API (Matriks, Foreks, Bloomberg vb.) önerilir.

## Seans Saatleri (Türkiye)

- Normal seans: **10:00 – 18:00**
- Öğle arası yok (sürekli seans)
- Tatiller: resmi tatiller + yarıyıl / yaz tatili günleri (basit takvim ile)

## Uyarı

Bu yazılım **eğitim ve araştırma** amaçlıdır. Yatırım tavsiyesi değildir. Otomatik alım-satım için ek risk yönetimi ve yasal gereklilikler vardır.

## Orijinal Proje

[InStock (GitHub)](https://github.com/myhhub/stock) — Çin A-hisseleri için geliştirilmişti.  
Bu sürüm Borsa İstanbul’a uyarlanmıştır.

## Lisans

Orijinal projenin lisansına uygun şekilde kullanılabilir (MIT benzeri).
