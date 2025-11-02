# JSON Creator - Montaj Kilavuzu Olusturucu

SolidWorks'ten export edilen STEP dosyalarindan otomatik JSON montaj kilavuzu olusturur.

## Kullanim

### 1. SolidWorks'ten Export

```
1. Assembly'yi ac
2. File → Save As
3. Save as type: STEP (*.stp)
4. Options →
   [✓] Export all components to separate files
   [✓] Save all components to one folder
5. Save
```

**Sonuc:** Tum parcalar ayri STEP dosyalari olarak kaydedilir!

### 2. JSON Creator'u Calistir

```bash
cd C:\depozito\uretim_planlama
conda activate montaj_kilavuzu
python tools/json_creator.py
```

### 3. STEP Klasoru Sec

1. "STEP Klasoru Sec" butonuna tiklayin
2. SolidWorks'ten export ettiginiz klasoru secin
3. Tum STEP dosyalari otomatik yuklenecek

### 4. Parcalari Duzenle

**Sol Panel - Parca Listesi:**
- Tum parcalar otomatik listelenir
- Parca ID'leri otomatik olusturulur (parca_001, parca_002, ...)

**Orta Panel - Parca Ozellikleri:**
- **Isim:** Parcaya anlamli isim verin
- **Renk:** "Renk Sec" ile 3D'de gorunecek rengi secin
- **Gorunurluk:** Baslangicta gorunur olsun mu?

### 5. Montaj Adimlari Olustur

**Sag Panel - Montaj Adimlari:**

1. "Adim Ekle" butonu
2. Her adim icin:
   - **Baslik:** Kisa aciklayici baslik
   - **Aciklama:** Detayli montaj talimati
   - **Sure:** Tahmini montaj suresi (saniye)
   - **Gorunur Parcalar:** Bu adimda hangi parcalar gorunsun
     - Ornek: `parca_001, parca_002, parca_003`
   - **Vurgulu Parcalar:** Hangi parcalar sari renkte vurgulansın
     - Ornek: `parca_002`

**Parca ID'lerini Nasil Bilirim?**
- Sol paneldeki listede her parcanin ID'si yazar
- Ornek: `parca_001 - Taban`

### 6. JSON Kaydet

1. "JSON Kaydet" butonuna tiklayin
2. Kayit yerini ve dosya adini secin
3. `data/assemblies/` klasorune kaydedin

### 7. 3D Uygulamada Test Edin

```bash
python main.py
```

1. Dosya → Montaj Ac
2. Olusturdug

unuz JSON'u secin
3. Montajiniz yuklenir!

## Ornek Workflow

```
SolidWorks Assembly
    ↓ (Export all components to separate files)
STEP Dosyalari (1000+ parca)
    ↓ (JSON Creator - 5 dakika)
montaj.json
    ↓ (3D Montaj Kilavuzu)
Interaktif 3D Kilavuz!
```

## Ipuclari

### Renk Secimi

Onerilen renkler:
- **Gri** (varsayilan): [0.7, 0.7, 0.7] - Genel parcalar
- **Mavi:** [0.2, 0.6, 1.0] - Ana govde parcalari
- **Kirmizi:** [1.0, 0.2, 0.2] - Onemli parcalar
- **Yesil:** [0.2, 0.8, 0.2] - Destek parcalari
- **Sari:** [1.0, 0.8, 0.0] - Uyari gerektiren parcalar

### Adim Planlamasi

1. **Adim 1:** Sadece taban/ilk parca
2. **Adim 2:** Taban + ikinci parca (ikinci parca vurgulu)
3. **Adim 3:** Onceki parcalar + yeni parca (yeni parca vurgulu)
4. ...son adimda tum parcalar gorunur

### Hizli Duzenleme

- Parca isimlerini anlamsiz tutun (dosya adlari kullanilir)
- Once tum parcalari yukleyin
- Sonra adim adim montaj sirasini planlayın
- Renkleri son adimda verin (opsiyonel)

## Sorun Giderme

**STEP dosyalari yuklenmiyor:**
- Klasorde .step veya .stp uzantili dosyalar var mi kontrol edin
- Dosya isimleri Turkce karakter icermiyorsa daha iyi

**Parca ID bulamiyorum:**
- Sol paneldeki listeye bakin
- Her satir: `parca_XXX - Dosya_Adi` formatinda

**JSON acilmiyor:**
- JSON dosyasini `data/assemblies/` klasorune kaydedin
- Dosya adinda Turkce karakter kullanmayin

## Gelecek Ozellikler

- [ ] Checkbox'li parca secimi (adimlar icin)
- [ ] Kamera pozisyonu on izleme
- [ ] Drag & drop ile adim siralaama
- [ ] SolidWorks API entegrasyonu (direkt .SLDASM okuma)
- [ ] 3D on izleme (VTK entegrasyonu)
