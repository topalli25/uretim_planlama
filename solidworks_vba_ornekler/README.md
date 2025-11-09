# SolidWorks VBA Örnekleri

Bu klasör, SolidWorks VBA öğrenmek ve montaj kilavuzu projesi için hazırlanmış örnek kodları içerir.

## 📚 İçerik

### 1. **01_Temel_Giris.swp** - Başlangıç Seviyesi
VBA'ya giriş ve temel SolidWorks API işlemleri.

**Örnekler:**
- ✅ Merhaba Dünya (SolidWorks versiyonu)
- ✅ Açık belge bilgisi alma
- ✅ Parça özellikleri (kütle, hacim, yüzey alanı)
- ✅ Tüm açık belgeleri listeleme
- ✅ Custom Property okuma/yazma
- ✅ Belge kaydetme
- ✅ Ekran yenileme kontrolü (performans)

**Öğrenecekleriniz:**
- SolidWorks API'ye bağlanma
- ModelDoc2, PartDoc, AssemblyDoc kullanımı
- Hata kontrolü (If Nothing Then...)
- Custom Property yönetimi
- Performans optimizasyonu

---

### 2. **02_Dosya_Islemleri.swp** - Orta Seviye
Dosya açma, kaydetme ve export işlemleri.

**Örnekler:**
- ✅ Parça açma (kod ile)
- ✅ Dosya seçici dialog ile parça açma
- ✅ STL export (binary/ASCII)
- ✅ STEP export (AP214 protokolü)
- ✅ Farklı isimle kaydet
- ✅ Klasördeki tüm parçaları STL'ye dönüştürme
- ✅ PDF export (çizim için)
- ✅ DXF/DWG export
- ✅ Dosya bilgisi raporlama

**Öğrenecekleriniz:**
- OpenDoc6 kullanımı
- SaveAs3 ve Export işlemleri
- Toplu dosya işlemleri
- FileSystemObject kullanımı
- Error handling

---

### 3. **03_STEP_To_STL_Montaj_Projesi.swp** - İleri Seviye ⭐
**Montaj kilavuzu projesi için özel geliştirilmiş VBA.**

**Ana Fonksiyon:** `MontajdanSTEPveSTLOlustur()`

**Ne Yapar:**
1. Açık montajdaki tüm parçaları tespit eder
2. Her parçayı ayrı ayrı STEP formatında export eder
3. Her STEP dosyasını STL'ye dönüştürür
4. İlerleme raporu gösterir
5. Log dosyası oluşturur

**Ek Fonksiyonlar:**
- `DogrudenSTLExport()` - STEP atla, doğrudan STL
- `ParcaListesiOlustur()` - Montaj parça listesi TXT

**Çıktılar:**
- `parca_001.step` - Her parça için STEP
- `parca_001.stl` - Her parça için STL
- `export_log.txt` - İşlem raporu
- `parca_listesi.txt` - Referans liste

**Performans:**
- 100 parça: ~2-3 dakika
- 500 parça: ~10-15 dakika
- 1000 parça: ~20-30 dakika

---

## 🚀 Nasıl Kullanılır?

### Adım 1: SolidWorks'te Macro Açma

1. **SolidWorks'ü açın**
2. **Tools → Macro → Edit** (veya Alt+F8)
3. İstediğiniz `.swp` dosyasını seçin
4. **VBA Editor** açılır

### Adım 2: Kodu Çalıştırma

**Yöntem A: Direkt çalıştırma**
- F5 tuşuna basın (veya Run → Run Sub/UserForm)
- İstediğiniz fonksiyonu seçin

**Yöntem B: Toolbar'dan**
- Tools → Macro → Run
- Macro'yu seçip çalıştırın

### Adım 3: Test Etme

Her örneği test etmek için:

**01_Temel_Giris.swp:**
1. SolidWorks'te bir parça açın
2. `ParcaOzellikleri()` makrosunu çalıştırın
3. Parça bilgilerini görün

**02_Dosya_Islemleri.swp:**
1. Bir parça açın
2. `STLExport()` makrosunu çalıştırın
3. STL dosyası oluşur

**03_STEP_To_STL_Montaj_Projesi.swp:**
1. Bir montaj açın (örn. 100 parça)
2. `MontajdanSTEPveSTLOlustur()` çalıştırın
3. Çıktı klasörü seçin
4. Bekleyin (~2-3 dakika)
5. STEP ve STL dosyaları hazır!

---

## 💡 Öğrenme Yolu

### Seviye 1: Temel (1-2 saat)
1. `01_Temel_Giris.swp` dosyasını açın
2. Her fonksiyonu tek tek çalıştırın
3. Kodları okuyun, yorumları inceleyin
4. Kendi versiyonunuzu yazın

### Seviye 2: Uygulama (2-3 saat)
1. `02_Dosya_Islemleri.swp` ile çalışın
2. STL, STEP export işlemlerini test edin
3. Kendi klasörünüzde toplu işlem yapın

### Seviye 3: Proje (3-4 saat)
1. `03_STEP_To_STL_Montaj_Projesi.swp` inceleyin
2. Küçük bir montajda test edin (10-20 parça)
3. Gerçek projenizde kullanın

**Toplam Öğrenme Süresi:** ~8-10 saat

---

## 🔗 Montaj Kilavuzu Projesinde Kullanım

### Tam İş Akışı

```
SolidWorks Montaj
     ↓
[VBA: 03_STEP_To_STL_Montaj_Projesi.swp]
     ↓
STEP + STL Dosyaları
     ↓
[Python: tools/json_creator.py]
     ↓
JSON Montaj Dosyası
     ↓
[Python: main.py]
     ↓
3D Montaj Kılavuzu
```

### Adım Adım

**1. SolidWorks'te Export (VBA)**
```vba
' Montajınızı açın
' Tools → Macro → Run
' 03_STEP_To_STL_Montaj_Projesi.swp → MontajdanSTEPveSTLOlustur()
' Çıktı klasörü: C:\proje\models\
```

**2. JSON Creator (Python)**
```bash
python tools/json_creator.py
# STEP Klasörü Seç → C:\proje\models\
# STL dosyaları otomatik yüklenir
# Montaj adımları oluştur
# JSON kaydet
```

**3. Ana Uygulama (Python)**
```bash
python main.py
# Dosya → Montaj Aç
# JSON'u seç ve görselleştir
```

---

## 📋 Çıktı Formatları

### STEP (.step)
- **Kullanım:** CAD program arası veri aktarımı
- **Protokol:** AP214 (renk ve katman bilgisi)
- **Boyut:** Orta (~500KB/parça)
- **Kalite:** En yüksek (parametrik)

### STL (.stl)
- **Kullanım:** Mesh görselleştirme, 3D printing
- **Format:** Binary (hızlı ve küçük)
- **Boyut:** Küçük (~200KB/parça)
- **Kalite:** Yüksek (triangulated mesh)

---

## ⚙️ Ayarlar ve Optimizasyon

### Performans İpuçları

**1. Ekran Güncellemesini Kapat**
```vba
swModel.FeatureManager.EnableFeatureTree = False
' ... İşlemler ...
swModel.FeatureManager.EnableFeatureTree = True
```

**2. Sessiz Mod Kullan**
```vba
swApp.OpenDoc6(dosya, swDocPART, swOpenDocOptions_Silent, "", errors, warnings)
```

**3. İlerleme Göster**
```vba
If (i Mod 10) = 0 Then
    swApp.SendMsgToUser2 "İşleniyor: " & i & "/" & toplam
    DoEvents
End If
```

### STEP Export Ayarları

**Yüksek Kalite:**
```vba
swApp.SetUserPreferenceIntegerValue swSTEPFormat, swSTEPFormat_AP214
swApp.SetUserPreferenceToggle swSTEPExportSurfacesAs, True
```

**STL Resolution:**
```vba
' Fine resolution (varsayılan)
swApp.SetUserPreferenceDoubleValue swSTLDeviation, 0.001
swApp.SetUserPreferenceDoubleValue swSTLAngleTolerance, 5.0
```

---

## 🐛 Hata Çözümleri

### "ActiveX component can't create object"
**Çözüm:** SolidWorks API'yi referans edin
1. VBA Editor → Tools → References
2. "SolidWorks 20XX Type Library" işaretleyin
3. OK

### "User-defined type not defined"
**Çözüm:** `Option Explicit` satırından sonra:
```vba
Dim swApp As Object
Set swApp = CreateObject("SldWorks.Application")
```

### "Permission denied" (Dosya kaydetme)
**Çözüm:**
- Klasörü kontrol edin (yazma izni var mı?)
- Dosya açık mı? (Kapatın)
- Yönetici olarak çalıştırın

### Yavaş çalışıyor
**Çözüm:**
- `EnableFeatureTree = False` kullanın
- `swOpenDocOptions_Silent` kullanın
- Gereksiz `ForceRebuild3` çağrılarını kaldırın

---

## 📚 Kaynaklar

### Resmi Dokümantasyon
- **SolidWorks API Help:** Help → API Help (F1)
- **Online:** https://help.solidworks.com/API/
- **Forum:** https://forum.solidworks.com/community/api

### Önerilen Öğrenme Sırası
1. API Help → Getting Started
2. Bu klasördeki örnekler (01 → 02 → 03)
3. SolidWorks Forum → API bölümü
4. Kendi projeleriniz

### VBA Temelleri
- **Microsoft VBA Dokümantasyonu**
- **Excel VBA** (benzer syntax)
- **Visual Basic 6.0** (aynı dil)

---

## 🎯 Sonraki Adımlar

Temel VBA'yı öğrendikten sonra:

1. **Özelleştirme**
   - Kendi makrolarınızı yazın
   - İş akışınıza özel fonksiyonlar

2. **Gelişmiş Konular**
   - FeatureManager kullanımı
   - Sketch API
   - Configuration yönetimi
   - Drawing automation

3. **Entegrasyon**
   - Python ile VBA entegrasyonu
   - External database bağlantısı
   - Excel raporlama

---

## 📞 Destek

**Soru ve Öneriler:**
- Kodları inceleyin, yorumlar detaylı
- Immediate Window'u kullanın (Ctrl+G)
- Debug.Print ile değişkenleri kontrol edin
- F8 ile adım adım çalıştırın

**Proje Dosyaları:**
```
solidworks_vba_ornekler/
├── README.md                           # Bu dosya
├── 01_Temel_Giris.swp                  # Başlangıç
├── 02_Dosya_Islemleri.swp              # Orta seviye
└── 03_STEP_To_STL_Montaj_Projesi.swp  # İleri seviye
```

---

## ✅ Başarı Kontrol Listesi

Öğrenme sürecinizi kontrol edin:

**Seviye 1:**
- [ ] VBA Editor'u açabildim
- [ ] İlk makromu çalıştırdım
- [ ] swApp ve swModel nedir anladım
- [ ] Custom Property okuyabildim
- [ ] Parça özelliklerini alabildim

**Seviye 2:**
- [ ] Dosya seçici dialog kullandım
- [ ] STL export edebildim
- [ ] STEP export edebildim
- [ ] Toplu işlem yapabiliyorum
- [ ] Hata kontrolü ekleyebildim

**Seviye 3:**
- [ ] Montaj componentlerini listeleyebildim
- [ ] Toplu STEP export yapabiliyorum
- [ ] STL dönüşümü otomatik çalışıyor
- [ ] Log dosyası oluşturabiliyorum
- [ ] 100+ parça işleyebildim

**Proje:**
- [ ] Kendi montajımda test ettim
- [ ] JSON Creator ile entegre ettim
- [ ] Ana uygulamada görselleştirdim
- [ ] Tam iş akışını tamamladım

---

**Kolay gelsin! VBA öğrenme yolculuğunuzda başarılar! 🚀**
