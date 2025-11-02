# JSON Creator - 3D Onizlemeli Kullanim Kilavuzu

## Genel Bakis

JSON Creator, SolidWorks'ten export edilen STEP dosyalarini otomatik olarak tarayip montaj kilavuzu JSON dosyasi olusturan gorsel bir aractir.

## Ozellikler

### 🎬 3D Onizleme
- Parcalari gercek zamanli 3D olarak goruntuleme
- Renk degisikliklerini canli izleme
- Tum montaji birden gorselestirme
- Adim onizleme (hangi parcalar gorunur/vurgulu)
- Kamera pozisyonu kaydetme

### 📦 Parca Yonetimi
- Otomatik STEP dosyasi tarama
- Akilli parca ID atama (parca_001, parca_002, ...)
- Parca arama/filtreleme
- Isim duzenleme
- Renk secimi (renk secici dialog)
- Gorunurluk ayari

### 📋 Montaj Adimlari
- Sinirsiz adim ekleme
- Her adim icin:
  - Baslik ve aciklama
  - Gorunur parcalar (virgul ile ayrilmis)
  - Vurgulu parcalar (sari renk)
  - Kamera pozisyonu
  - Sure (saniye)
- Adim onizleme (3D'de gosterme)

## Kullanim Adimlari

### 1. SolidWorks'ten STEP Export

SolidWorks'te montajinizi acin:
1. **File → Save As → STEP (*.step)**
2. **Options → Export all components to separate files** secin
3. AP214 veya AP203 protokolunu secin
4. Tum parcalari ayri bir klasore kaydedin

### 2. JSON Creator'i Baslatma

```bash
# Virtual environment aktif et
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# JSON Creator'i calistir
python tools/json_creator.py
```

### 3. STEP Klasoru Secimi

1. **"📂 STEP Klasoru Sec"** butonuna tiklayin
2. SolidWorks'ten export ettiginiz klasoru secin
3. Program otomatik olarak tum .step/.stp dosyalarini tarayacak
4. Sol panelde parca listesi olusacak

**Ornek:**
```
Toplam: 127 parca
parca_001 - taban
parca_002 - govde_ana
parca_003 - kapak_ust
...
```

### 4. Parcalari Gorselestirme

#### Tek Parca Gosterme
1. Sol panelden bir parca secin
2. Otomatik olarak 3D gorunumde goreceksiniz
3. Model bilgisi (nokta, yuzey, hacim) gorunecek

#### Tum Parcalari Gosterme
1. **"👁 Hepsini Goster"** butonuna tiklayin
2. Tum parcalar 3D sahnede yuklenecek
3. 1000+ parca icin cache sistemi kullanilir (hizli)

#### Parca Ozellikleri Duzenleme
"✏️ Parca Duzenle" sekmesinde:
- **Isim:** Parca adini degistirin
- **Renk:** 🎨 butonu ile renk secin (3D'de canli guncellenir)
- **Gorunurluk:** Baslangicta gorunur mu?

### 5. Montaj Adimlari Olusturma

#### Yeni Adim Ekleme
1. Sag panelde **"➕ Adim Ekle"** tiklayin
2. Adim formu acilacak

#### Adim Ozellikleri
```
Baslik: Adim 1: Tabani Monte Et
Aciklama: Taban parcasini is tezgahina yerlestirin...
Sure: 60 saniye

Gorunur Parcalar: parca_001, parca_002, parca_003
Vurgulu Parcalar: parca_001

Kamera Pozisyonu: [100, 100, 100]
```

#### Kamera Pozisyonu Kaydetme
1. 3D gorunumde kamerayi istediginiz aciya getirin
2. Adimi secin
3. **"📷 Kamera Pozisyonu Kaydet"** butonuna tiklayin
4. Mevcut kamera pozisyonu adima kaydedilir

#### Adim Onizleme
1. Adimi secin
2. **"👁 Onizle"** butonuna tiklayin
3. 3D gorunumde tam olarak nasil gorunecegini goreceksiniz:
   - Gorunur parcalar yuklenir
   - Vurgulu parcalar SARI renkte gosterilir
   - Kamera otomatik ayarlanir

### 6. JSON Kaydetme

1. **"💾 JSON Kaydet"** butonuna tiklayin
2. Kayit yerini secin (ornek: `data/assemblies/montaj_proje1.json`)
3. JSON dosyasi olusturulacak

**Olusturulan JSON yapisi:**
```json
{
  "isim": "montaj_proje1",
  "aciklama": "127 parcali montaj",
  "parcalar": [
    {
      "id": "parca_001",
      "isim": "Taban",
      "model_dosyasi": "taban.step",
      "renk": [0.7, 0.7, 0.7],
      "gorunur": true
    }
  ],
  "adimlar": [
    {
      "adim_numarasi": 1,
      "baslik": "Adim 1: Tabani Monte Et",
      "aciklama": "...",
      "gorunur_parcalar": ["parca_001", "parca_002"],
      "vurgulu_parcalar": ["parca_001"],
      "kamera_pozisyonu": [100, 100, 100],
      "sure": 60
    }
  ]
}
```

### 7. Ana Uygulamada Kullanma

JSON'u kaydetikten sonra ana uygulamada test edin:

```bash
python main.py
```

1. **Dosya → Montaj Ac...**
2. Olusturdugu JSON'u secin
3. 3D gorunum yuklenir
4. Adimlari test edin

## İpuclari

### 1000+ Parca icin Performans
- JSON Creator akilli cache kullanir
- Bir kez yuklenen meshler hafizada tutulur
- "Hepsini Goster" butonu tum parcalari ilerleme ile yukler
- 10'ar parca araliginda ilerleme gosterilir

### Hizli İs Akisi
1. STEP klasorunu sec
2. "Hepsini Goster" ile genel kontrolu yap
3. Parcalari gerekirse yeniden adlandir/renklendir
4. Adimlari olustur (gorunur/vurgulu parcalari belirt)
5. Her adim icin "Onizle" ile kontrol et
6. Kamera pozisyonunu kaydet
7. JSON'u kaydet
8. Ana uygulamada test et

### Arama/Filtreleme
- Sol paneldeki arama kutusunu kullanin
- Parca ID veya isim ile arayabilirsiniz
- Ornek: "govde" yazarsa sadece govde iceren parcalar gosterilir

### Renk Yonetimi
- Her parca farkli renk alabilir
- Renk secici ile RGB/HSV olarak secilebilir
- Degisiklik 3D gorunumde canli yansir
- Ayni turdeki parcalari ayni renk yapabilirsiniz

### Vurgulama Stratejisi
- **Gorunur parcalar:** O adimda montajda olmasi gereken parcalar
- **Vurgulu parcalar:** O adimda MONTE EDILECEK parcalar (sari)
- Ornek: Adim 3'te parca_001,002,003 gorunur ama sadece parca_003 vurgulu (yeni ekleniyor)

## Sorun Giderme

### "ModuleNotFoundError: PyQt6"
```bash
pip install PyQt6
```

### "Model yuklenemedi" hatasi
- STEP dosyasinin bozuk olmadigini kontrol edin
- Dosya yolunda Turkce karakter olmasin
- AP214 veya AP203 formatinda export edilmis olmali

### "Klasorde STEP dosyasi bulunamadi"
- .step veya .stp uzantili dosyalarin oldugunu kontrol edin
- Buyuk/kucuk harf farki olabilir (.STEP vs .step)

### 3D gorunum bos
- VTK kurulumunu kontrol edin: `pip install vtk`
- Mesh boyutlarinin dogru oldugunu kontrol edin
- "Kamera Sifirla" butonunu deneyin

## Ornek Senaryo

1000 parcali bir montaj icin:

```
1. SolidWorks'ten 1000 parca ayri ayri STEP export edildi
2. JSON Creator acildi
3. Klasor secildi → 1000 parca yuklendi (5 saniye)
4. "Hepsini Goster" → Tum montaj goruldu (30 saniye)
5. Parcalar yeniden adlandirildi (gerekliyse)
6. 15 adim olusturuldu:
   - Her adim icin gorunur/vurgulu parcalar belirlendi
   - Kamera pozisyonlari kaydedildi
   - Adimlar onizlendi
7. JSON kaydedildi (2 MB)
8. Ana uygulamada test edildi → Basarili!
```

## Gelecek Ozellikler

- [ ] Adim kopyalama/yapislandirma
- [ ] Parca grubu olusturma (alt montajlar)
- [ ] JSON sablonlari
- [ ] Toplu renk degistirme
- [ ] Video export (adim adim animasyon)
- [ ] SolidWorks VBA entegrasyonu (otomatik export)

---

**Son Guncelleme:** 2025-11-02
**Versiyon:** 1.1 (3D Onizlemeli)
