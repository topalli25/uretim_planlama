# 3D Montaj Kılavuzu Uygulaması

SolidWorks CAD dosyalarından oluşturulan 3D modelleri görselleştiren ve adım adım montaj talimatları sunan masaüstü uygulaması.

## Özellikler

- ✅ 3D model görselleştirme (STL/STEP desteği)
- ✅ Adım adım montaj talimatları
- ✅ Alt montaj yönetimi
- ✅ Parça seçimi ve vurgulama
- ✅ Kiosk modu (tam ekran)
- ✅ 1000+ parça desteği

## Teknoloji

- **Python 3.10+**
- **PyQt6** - GUI framework
- **VTK** - 3D görselleştirme
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
├── main.py                 # Ana uygulama
├── requirements.txt        # Gerekli paketler
├── config.json            # Ayarlar
├── src/
│   ├── gui/               # GUI bileşenleri
│   ├── core/              # İş mantığı
│   └── utils/             # Yardımcı fonksiyonlar
├── data/
│   ├── models/            # 3D model dosyaları
│   └── assemblies/        # Montaj tanımları (JSON)
└── assets/                # Görseller ve stiller
```

## Geliştirici

Proje geliştirilme aşamasındadır.
