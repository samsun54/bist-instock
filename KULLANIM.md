# BIST-InStock Kullanım Kılavuzu

## 1. Kurulum

```bash
cd bist-instock
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### TA-Lib (isteğe bağlı, daha fazla indikatör için)

Ubuntu/Debian:
```bash
sudo apt-get install -y build-essential wget
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib && ./configure --prefix=/usr && make && sudo make install
pip install TA-Lib
```

TA-Lib yoksa sistem otomatik olarak pandas tabanlı basit indikatörlere (MA, RSI, MACD, Bollinger, ATR) geçer.

## 2. Komutlar

### Günlük veri çek
```bash
python -m bist.job.fetch_daily
python -m bist.job.fetch_daily --universe bist100
python -m bist.job.fetch_daily --codes THYAO,GARAN,ASELS,TUPRS
```

### İndikatör hesapla
```bash
python -m bist.job.calc_indicators --code THYAO
python -m bist.job.calc_indicators --code GARAN.IS --period 6mo
```

### Strateji tara
```bash
python -m bist.job.run_strategies
python -m bist.job.run_strategies --universe bist100
```

## 3. Stratejiler

| Anahtar        | Açıklama                                      |
|----------------|-----------------------------------------------|
| hacim_artisi   | Hacim ≥ 2× 5 günlük ortalama + yükseliş       |
| ma_yukselis    | MA30 yükseliyor ve fiyat MA üzerinde          |
| turtle         | Son kapanış son 20 günün en yükseği           |
| ma_kirilim     | Fiyat 60 günlük MA'yı yukarı kesiyor + hacim  |

## 4. Veri klasörü

- `data/` → CSV çıktılar (spot, indikatör, strateji sonuçları)
- `cache/hist/` → yfinance geçmiş veri önbelleği (6 saat)

## 5. Seans

- İşlem günü: hafta içi (Cumartesi-Pazar + sabit resmi tatiller hariç)
- Seans: 10:00 – 18:00 (Türkiye saati)
- `bist.lib.trade_time` modülünden kontrol edilebilir

## 6. Sınırlamalar

- yfinance ücretsizdir; gecikme veya eksik veri olabilir.
- Bazı eski BIST kodları yfinance’te yoktur (listeyi güncelleyin).
- Orijinal projedeki Çin’e özgü özellikler (龙虎榜, 涨停, East Money) kaldırılmıştır.
- Otomatik alım-satım / broker entegrasyonu yoktur.

## 7. Genişletme

Yeni strateji eklemek için `bist/core/strategy/strategies.py` içine fonksiyon yazıp `run_all_strategies` sözlüğüne ekleyin.

Yeni hisse listesi: `bist/core/bist_symbols.py`.
