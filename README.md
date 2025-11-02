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

### Ana Uygulama
```bash
python main.py
```

### JSON Creator (3D Onizlemeli)
SolidWorks STEP dosyalarindan montaj JSON olusturmak icin:

```bash
python tools/json_creator.py
```

**Ozellikler:**
- 3D parca onizleme
- Canli renk guncelleme
- Adim onizleme ve kamera pozisyonu kaydetme
- 1000+ parca desteği (cache sistemi)
- Akilli arama/filtreleme

Detayli kullanim: [docs/JSON_CREATOR_KULLANIM.md](docs/JSON_CREATOR_KULLANIM.md)

## Proje Yapısı

```
montaj_kilavuzu/
├── main.py                      # Ana uygulama
├── requirements.txt             # Gerekli paketler
├── config.json                  # Ayarlar
├── src/
│   ├── gui/                     # GUI bileşenleri
│   │   ├── ana_pencere.py       # Ana pencere (ASCII)
│   │   ├── gorunum_widget.py    # 3D görünüm widget (VTK)
│   │   └── kontrol_paneli.py    # Kontrol paneli
│   ├── core/                    # İş mantığı
│   │   ├── model_yukleyici.py   # STEP/STL yükleyici
│   │   ├── montaj_yoneticisi.py # Montaj yönetimi
│   │   └── adim_yoneticisi.py   # Adım kontrolü
│   └── utils/                   # Yardımcı fonksiyonlar
│       └── yardimcilar.py       # Yardımcı fonksiyonlar
├── tools/
│   └── json_creator.py          # JSON Creator GUI (3D önizlemeli)
├── docs/
│   └── JSON_CREATOR_KULLANIM.md # JSON Creator kullanım kılavuzu
├── data/
│   ├── models/                  # 3D model dosyaları (STEP/STL)
│   └── assemblies/              # Montaj tanımları (JSON)
└── tests/                       # Test dosyaları
    └── create_sample_models.py  # Örnek STL oluşturucu
```

## Sorun Giderme

### STEP Dosya Yukleme Hatasi

Eger "File type: step not supported" hatasi aliyorsaniz:

**Hizli Cozum:**
```bash
# Ek kutuphaneler yukleyin
pip install trimesh[easy] pyassimp networkx
```

**Onerilir Cozum:** STEP dosyalarini STL'ye donusturun
```bash
# Toplu donusturme araci
python tools/step_to_stl_converter.py /path/to/step/klasoru
```

**Detayli kilavuz:** [docs/STEP_DOSYA_SORUNLARI.md](docs/STEP_DOSYA_SORUNLARI.md)

### Diger Sorunlar

- **Windows encoding:** Tum kod dosyalari ASCII karakterler kullanir
- **VTK kurulumu:** `pip install vtk`
- **PyQt6 kurulumu:** `pip install PyQt6`

## Dokumantasyon

- [README.md](README.md) - Genel bilgi
- [docs/JSON_CREATOR_KULLANIM.md](docs/JSON_CREATOR_KULLANIM.md) - JSON Creator kilavuzu
- [docs/STEP_DOSYA_SORUNLARI.md](docs/STEP_DOSYA_SORUNLARI.md) - STEP yukleme sorunlari
- [CHANGELOG.md](CHANGELOG.md) - Versiyon gecmisi
- [PROJE_DURUMU.md](PROJE_DURUMU.md) - Proje raporu

## Geliştirici

Proje geliştirilme aşamasındadır.
