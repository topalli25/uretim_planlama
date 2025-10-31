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

### 5. Örnek STL Dosyalarını Oluşturun

```bash
python tests/create_sample_models.py
```

Bu komut `data/models/` klasörüne 5 adet örnek STL dosyası oluşturacak.

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

### 1. STL Dosyalarını Ekleyin

SolidWorks'ten parçalarınızı STL formatında export edin ve `data/models/` klasörüne kopyalayın.

### 2. Montaj JSON Dosyası Oluşturun

`data/assemblies/` klasöründe yeni bir JSON dosyası oluşturun:

```json
{
  "name": "Kendi Montajım",
  "description": "Açıklama",
  "parts": [
    {
      "id": "part_001",
      "name": "Parça Adı",
      "model_file": "parca.stl",
      "color": [0.8, 0.8, 0.8],
      "visible": true
    }
  ],
  "steps": [
    {
      "step_number": 1,
      "title": "Adım 1",
      "description": "Adım açıklaması",
      "visible_parts": ["part_001"],
      "highlight_parts": ["part_001"],
      "camera_position": [100, 100, 100],
      "duration": 60
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

### STL Dosyaları Yüklenmiyor

- Dosya yollarının doğru olduğundan emin olun
- STL dosyalarının binary veya ASCII formatında olduğunu kontrol edin
- SolidWorks'ten export ederken "Binary" STL seçin (daha küçük dosya)

## Kiosk Modu

Tam ekran kiosk modu için:
1. **F11** tuşuna basın veya
2. Menüden **Görünüm → Tam Ekran** seçin

`config.json` dosyasında `"fullscreen": true` yaparak varsayılan tam ekran yapabilirsiniz.

## Performans İpuçları

1000+ parça için:
- STL dosyalarını binary formatında kaydedin
- Parça sayısını azaltmak için alt montajları birleştirin
- Çok detaylı mesh'leri basitleştirin (Decimate)
- `config.json`'da antialiasing'i kapatın: `"enable_antialiasing": false`

## Klavye Kısayolları

- **F11:** Tam ekran
- **R:** Kamerayı sıfırla
- **Ctrl+O:** Montaj aç
- **Ctrl+Q:** Çıkış
- **← →:** Önceki/Sonraki adım (gelecekte eklenecek)

## Destek

Sorun bildirmek veya öneride bulunmak için GitHub Issues kullanın.
