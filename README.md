# 3D Montaj Kılavuzu Uygulaması

SolidWorks CAD dosyalarından oluşturulan 3D modelleri görselleştiren ve adım adım montaj talimatları sunan masaüstü uygulaması.

## Özellikler

- ✅ 3D model görselleştirme (STEP/STL desteği - STEP öncelikli)
- ✅ Adım adım montaj talimatları
- ✅ Alt montaj yönetimi
- ✅ Parça seçimi ve vurgulama
- ✅ Kiosk modu (tam ekran)
- ✅ 1000+ parça desteği
- ✅ Türkçe kod yapısı ve arayüz

## Teknoloji

- **Python 3.10+**
- **PyQt6** - GUI framework
- **VTK** - 3D görselleştirme (native performans)
- **trimesh** - 3D dosya işleme

## Kurulum

```bash
# Virtual environment oluştur
python -m venv venv

# Aktif et (Linux/Mac)
source venv/bin/activate

# Aktif et (Windows)
venv\Scripts\activate

# Bağımlılıkları kur
pip install -r requirements.txt
```

## Kullanım

```bash
python main.py
```

## Proje Yapısı

```
montaj_kilavuzu/
├── main.py                      # Ana uygulama
├── requirements.txt             # Gerekli paketler
├── config.json                  # Ayarlar
├── src/
│   ├── gui/                     # GUI bileşenleri
│   │   ├── ana_pencere.py       # Ana pencere (Türkçe)
│   │   ├── gorunum_widget.py    # 3D görünüm widget
│   │   └── kontrol_paneli.py    # Kontrol paneli
│   ├── core/                    # İş mantığı
│   │   ├── model_yukleyici.py   # STEP/STL yükleyici
│   │   ├── montaj_yoneticisi.py # Montaj yönetimi
│   │   └── adim_yoneticisi.py   # Adım kontrolü
│   └── utils/                   # Yardımcı fonksiyonlar
│       └── yardimcilar.py       # Türkçe yardımcı fonksiyonlar
├── data/
│   ├── models/                  # 3D model dosyaları (STEP/STL)
│   └── assemblies/              # Montaj tanımları (JSON)
└── tests/                       # Test dosyaları
```

## Geliştirici

Proje geliştirilme aşamasındadır.
