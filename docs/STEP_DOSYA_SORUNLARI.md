# STEP Dosya Yukleme Sorunlari - Cozum Kilavuzu

## Problem

JSON Creator veya ana uygulamada STEP dosyalari yuklenirken su hata aliyor:

```
Hata [parca_XXX]: Model yuklenirken hata: File type: step not supported
```

## Neden Oluyor?

Python'da STEP dosyalarini okumak icin ek kutuphaneler gerekir. trimesh kutuphanesi varsayilan olarak sadece STL, OBJ gibi mesh formatlarini destekler. STEP gibi CAD formatlarini okumak icin:

1. **pyassimp** - CAD dosya okuma kutuphanesi
2. **FreeCAD Python API** - En iyi kalite ama kurulum zor
3. **python-occ** - Profesyonel CAD islemleri (cok buyuk, karmasik)

## HIZLI COZUM: STL Formatina Donustur

En pratik ve guvenilir cozum STEP dosyalarinizi STL formatina donusturmektir.

---

## Cozum 1: SolidWorks ile Donusturme (ONERILIR)

SolidWorks'te halihazirda parcalariniz var, en kolay yontem:

### Tek Parca Donusturme

1. **SolidWorks'te parcayi acin**
2. **File → Save As**
3. **"Save as type"** kisminda **STL (*.stl)** secin
4. **Options** butonuna tiklayin:
   ```
   Resolution: Fine
   Output as: Binary
   Unit: Millimeters
   ```
5. **OK** → **Save**

### Toplu Donusturme (1000+ Parca)

Montajinizi zaten parcalara ayirmistiniz ("Export all components to separate files").
Simdi bunlari STL'ye donusturmek icin:

#### Yontem A: SolidWorks Macro (Otomatik)

1. SolidWorks'te **Tools → Macro → New**
2. Su kodu yapislandirin:

```vba
' STEP'ten STL'ye toplu donusturucu
Sub StepToStlConverter()
    Dim swApp As SldWorks.SldWorks
    Dim swModel As SldWorks.ModelDoc2
    Dim stepFolder As String
    Dim stlFolder As String
    Dim fileName As String

    Set swApp = Application.SldWorks

    ' Klasor secimi
    stepFolder = "C:\path\to\step\files\"
    stlFolder = "C:\path\to\stl\output\"

    ' Klasordeki her STEP dosyasi icin
    fileName = Dir(stepFolder & "*.step")

    Do While fileName <> ""
        ' STEP ac
        Set swModel = swApp.OpenDoc6(stepFolder & fileName, _
            swDocPART, swOpenDocOptions_Silent, "", 0, 0)

        ' STL kaydet
        swModel.SaveAs3 stlFolder & Replace(fileName, ".step", ".stl"), _
            0, 0

        ' Kapat
        swApp.CloseDoc fileName

        ' Sonraki dosya
        fileName = Dir()
    Loop

    MsgBox "Tamamlandi!"
End Sub
```

3. **Macro → Run**

#### Yontem B: Manuel Her Parcayi Ac-Kaydet

Eger 100'den az parca varsa:
1. Her STEP dosyasini ac
2. File → Save As → STL
3. Kaydet

---

## Cozum 2: FreeCAD ile Donusturme (UCRETSIZ)

FreeCAD ucretsiz ve cok guclu bir CAD yazilimi.

### Kurulum

1. FreeCAD'i indirin: https://www.freecad.org/downloads.php
2. Windows icin: FreeCAD-0.21.x-Windows-x86_64-installer.exe
3. Kurun

### Tek Dosya Donusturme

1. **File → Open** → STEP dosyasini secin
2. Parca yuklenir
3. **File → Export → Mesh Formats**
4. **Dosya turu:** STL Mesh (*.stl)
5. **Kaydet**

### Toplu Donusturme (Python Script)

FreeCAD Python console'unda (View → Panels → Python console):

```python
import FreeCAD
import Mesh
import Import
import os

# Klasorler
step_klasor = "C:/path/to/step/files/"
stl_klasor = "C:/path/to/stl/output/"

# Her STEP dosyasi icin
for dosya in os.listdir(step_klasor):
    if dosya.endswith('.step') or dosya.endswith('.stp'):
        print(f"Donusturuluyor: {dosya}")

        # STEP yukle
        doc = FreeCAD.newDocument()
        Import.insert(step_klasor + dosya, doc.Name)

        # Mesh'e cevir ve kaydet
        for obj in doc.Objects:
            if hasattr(obj, 'Shape'):
                mesh = Mesh.Mesh(obj.Shape.tessellate(0.1))
                stl_dosya = stl_klasor + dosya.replace('.step', '.stl')
                mesh.write(stl_dosya)
                print(f"  Kaydedildi: {stl_dosya}")
                break

        FreeCAD.closeDocument(doc.Name)

print("Tamamlandi!")
```

---

## Cozum 3: Bizim Converter Script'imiz

Projede hazir bir script var:

```bash
python tools/step_to_stl_converter.py /path/to/step/klasoru
```

**Ozellikler:**
- Otomatik toplu donusturme
- FreeCAD veya trimesh kullanir
- Zaten var olan STL'leri atlar
- Ilerleme raporu verir

**Kullanim:**

```bash
# Otomatik (her yontemi dene)
python tools/step_to_stl_converter.py /path/to/klasor

# Sadece FreeCAD (en iyi kalite)
python tools/step_to_stl_converter.py --freecad /path/to/klasor

# Manuel kilavuz
python tools/step_to_stl_converter.py --help-manual
```

---

## Cozum 4: Online Donusturucu (Hizli Test)

Kucuk projeler veya test icin online araclari kullanabilirsiniz:

- https://www.convertonline.io/convert/step-to-stl
- https://products.aspose.app/3d/conversion/step-to-stl
- https://www.cadexchanger.com/

**UYARI:** Gizli/ozel projelerinizi online yuklemeyin!

---

## Cozum 5: Python Kutuphanelerini Yukle (Gelismis)

STEP dosyalarini dogrudan Python'da okumak isterseniz:

### Yontem A: pyassimp (Kolay)

```bash
pip install pyassimp
pip install trimesh[easy]
```

Sonra uygulamayi yeniden calistirin.

### Yontem B: pythonocc (Profesyonel, Zor)

```bash
conda install -c conda-forge pythonocc-core
```

**NOT:** Bu yontem karmasik ve buyuk kurulum gerektirir (2GB+).

---

## Onerimiz

**En iyi cozum:** STEP dosyalarini STL'ye donusturmek

**Sebep:**
1. ✅ STL evrensel mesh formati - her uygulama acar
2. ✅ Daha hizli yuklenr (binary format)
3. ✅ Daha kucuk dosyalar (optimizasyon mumkun)
4. ✅ Kutlphane bagimlilik problemi yok
5. ✅ Windows/Linux/Mac uyumlu

**STEP'i Ne Zaman Kullanalim:**
- Orijinal CAD verisi gerektiginde
- Parametrik duzenleme yapilacaksa
- Yuksek hassasiyet gerektiyorsa

**STL'yi Ne Zaman Kullanalim:**
- Sadece gorselestirme icin
- Montaj kilavuzu (bizim durumumuz)
- 3D printing
- Web gorsellestirme

---

## Uygulamamizin Davranisi

Guncellenmis `model_yukleyici.py` su mantikla calisir:

```
1. STEP dosyasi yuklemeye calis
   ├─ Basarili → Kullan
   └─ Basarisiz → Ayni isimde STL var mi?
       ├─ Varsa → STL'yi kullan (otomatik)
       └─ Yoksa → Detayli hata mesaji goster
```

**Ornek:**
```
/models/
├── parca_001.step
├── parca_001.stl    ← Otomatik kullanilir
├── parca_002.step
└── parca_002.stl    ← Otomatik kullanilir
```

Program once STEP'i dener, basarisiz olursa ayni isimdeki STL'yi otomatik kullanir.

---

## Adim Adim: Projenizi Calistirma

### 1. SolidWorks'te Hazirlik

```
1. Montajinizi acin
2. File → Save As → STEP
3. Options → "Export all components to separate files"
4. Kaydedin (ornek: C:\proje\step_files\)
```

### 2. STL'ye Donusturme

**SECIM A:** SolidWorks Macro (yukarda)
**SECIM B:** FreeCAD Script (yukarda)
**SECIM C:** Bizim script:

```bash
cd /path/to/uretim_planlama
python tools/step_to_stl_converter.py C:\proje\step_files\
```

### 3. JSON Creator'da Kullan

```bash
python tools/json_creator.py
```

1. **"STEP Klasoru Sec"** → `C:\proje\step_files\` secin
2. Program otomatik olarak STL dosyalarini yukleyecek
3. Eger .step ve .stl beraber varsa STL tercih edilir
4. JSON olusturun

### 4. Ana Uygulamada Test

```bash
python main.py
```

1. File → Montaj Ac
2. Olusturdunuz JSON'u secin
3. Basarili!

---

## Sikca Sorulan Sorular

### S: STEP mi STL mi daha iyi?

**Cevap:** Montaj kilavuzu icin STL daha pratik. STEP CAD islemleri icin daha iyi.

### S: STL donusumunde kalite kaybediyor mu?

**Cevap:** Resolution ayarini "Fine" yaparsaniz goz ile fark edilmez. Binary format kullanin (daha kucuk).

### S: 1000 parcayi nasil hizlica donustururum?

**Cevap:**
1. SolidWorks VBA macro (en hizli)
2. FreeCAD Python script
3. Bizim converter tool

### S: Hem STEP hem STL dosyam var, hangisi kullanilir?

**Cevap:** Program once STEP'i dener. Basarisiz olursa STL'yi otomatik kullanir.

### S: pyassimp kurunca STEP okuyabilir miyim?

**Cevap:** Bazen calisir ama garantili degil. STL'ye donusturme daha guvenilir.

### S: Online donusturucu guvenli mi?

**Cevap:** Genel projeler icin evet. Gizli/patent projeler icin HAYIR - lokal donusturun.

---

## Ozet

| Yontem | Hiz | Kalite | Kolay | Onerilir |
|--------|-----|--------|-------|----------|
| SolidWorks → STL | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ EN IYISI |
| FreeCAD Script | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ Ucretsiz |
| Bizim Tool | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ Hizli test |
| Online | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⚠️ Dikkat |
| pyassimp | ⭐ | ⭐⭐ | ⭐ | ❌ Riskli |

---

**Yardima ihtiyaciniz varsa:** Bu dokumantasyonu takip edin veya `tools/step_to_stl_converter.py --help-manual` calistirin.
