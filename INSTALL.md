# Kurulum Talimatları

## Sistem Gereksinimleri

- **Python:** 3.10 veya üzeri
- **İşletim Sistemi:** Windows 10/11, Linux, macOS
- **RAM:** Minimum 4GB (1000+ parça için 8GB+ önerilir)
- **Grafik:** OpenGL 3.2+ destekli ekran kartı

## Adım Adım Kurulum

### 1. Python Kurulumu

Python yüklü değilse:
- **Windows:** https://www.python.org/downloads/ adresinden indirin
- **Linux:** `sudo apt install python3 python3-pip python3-venv`
- **macOS:** `brew install python3`

Kurulumu kontrol edin:
```bash
python --version
```

### 2. Proje Klasörüne Gidin

```bash
cd /home/user/uretim_planlama
```

### 3. Virtual Environment Oluşturun

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### 4. Bağımlılıkları Kurun

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Not:** VTK kurulumu biraz zaman alabilir (500MB+).

### 5. Örnek STEP Dosyalarını Oluşturun

```bash
python tests/create_sample_models.py
```

Bu komut `data/models/` klasörüne 5 adet örnek STEP dosyası (ve yedek STL) oluşturacak.

### 6. Uygulamayı Çalıştırın

```bash
python main.py
```

## İlk Kullanım

1. Uygulama açıldığında menüden **Dosya → Montaj Aç...** seçin
2. `data/assemblies/ornek_montaj.json` dosyasını seçin
3. 5 parçalı örnek montaj yüklenecektir
4. Sağ panelden adımlar arasında gezinin
5. **Sonraki ▶** butonu ile montaj adımlarını takip edin

## Kendi Montajınızı Oluşturma

### 1. STEP Dosyalarını Ekleyin

SolidWorks'ten parçalarınızı **STEP formatında** export edin ve `data/models/` klasörüne kopyalayın.

**Önerilen:** STEP formatı (.step veya .stp) - daha zengin geometri bilgisi
**Alternatif:** STL formatı (.stl) - basit mesh formatı

### 2. Montaj JSON Dosyası Oluşturun (Türkçe Anahtarlar)

`data/assemblies/` klasöründe yeni bir JSON dosyası oluşturun:

```json
{
  "isim": "Kendi Montajım",
  "aciklama": "Açıklama",
  "parcalar": [
    {
      "id": "parca_001",
      "isim": "Parça Adı",
      "model_dosyasi": "parca.step",
      "renk": [0.8, 0.8, 0.8],
      "gorunur": true
    }
  ],
  "adimlar": [
    {
      "adim_numarasi": 1,
      "baslik": "Adım 1",
      "aciklama": "Adım açıklaması",
      "gorunur_parcalar": ["parca_001"],
      "vurgulu_parcalar": ["parca_001"],
      "kamera_pozisyonu": [100, 100, 100],
      "sure": 60
    }
  ]
}
```

### 3. Renk Kodları

RGB renkleri 0-1 arası değerlerle:
- Kırmızı: `[1.0, 0.0, 0.0]`
- Yeşil: `[0.0, 1.0, 0.0]`
- Mavi: `[0.0, 0.0, 1.0]`
- Gri: `[0.8, 0.8, 0.8]`
- Beyaz: `[1.0, 1.0, 1.0]`

## Sorun Giderme

### VTK Kurulumu Başarısız Olursa

```bash
pip install --upgrade pip setuptools wheel
pip install vtk --no-cache-dir
```

### PyQt6 Hataları

Linux'ta ek paketler gerekebilir:
```bash
sudo apt install libxcb-cursor0 libxcb-xinerama0
```

### "Module not found" Hatası

Virtual environment'ın aktif olduğundan emin olun:
```bash
which python  # Linux/Mac
where python  # Windows
```

### STEP/STL Dosyaları Yüklenmiyor

- Dosya yollarının doğru olduğundan emin olun
- STEP dosyaları için `.step` veya `.stp` uzantısı kullanın
- STL dosyalarının binary veya ASCII formatında olduğunu kontrol edin
- SolidWorks'ten export ederken:
  - **STEP:** AP214 veya AP203 formatı seçin
  - **STL:** "Binary" STL seçin (daha küçük dosya)

## Kiosk Modu

Tam ekran kiosk modu için:
1. **F11** tuşuna basın veya
2. Menüden **Görünüm → Tam Ekran** seçin

`config.json` dosyasında `"fullscreen": true` yaparak varsayılan tam ekran yapabilirsiniz.

## Performans İpuçları

1000+ parça için:
- **STEP formatı kullanın** - daha optimize geometri
- Parça sayısını azaltmak için alt montajları birleştirin
- SolidWorks'te parçaları basitleştirin (küçük detayları kaldırın)
- Çok detaylı mesh'leri basitleştirin (Decimate)
- `config.json`'da antialiasing'i kapatın: `"enable_antialiasing": false`

**Not:** VTK native performans sağlar, bu nedenle 1000+ parça için web tabanlı çözümlerden çok daha hızlıdır.

## Klavye Kısayolları

- **F11:** Tam ekran
- **R:** Kamerayı sıfırla
- **Ctrl+O:** Montaj aç
- **Ctrl+Q:** Çıkış
- **← →:** Önceki/Sonraki adım (gelecekte eklenecek)

## Destek

Sorun bildirmek veya öneride bulunmak için GitHub Issues kullanın.
