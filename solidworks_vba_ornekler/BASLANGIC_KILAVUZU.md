# 🚀 SolidWorks VBA - Hızlı Başlangıç Kılavuzu

## ⚠️ ÖNEMLİ: VBA Dosyalarını Doğru Kullanma

SolidWorks VBA kodları **direkt dosyadan çalıştırılamaz**. Kodu kopyalayıp VBA Editor'e yapıştırmanız gerekir.

---

## 📋 YÖNTEM 1: Kopyala-Yapıştır (ÖNERİLİR)

### Adım 1: SolidWorks VBA Editor'ü Açın

1. **SolidWorks'ü açın**
2. **Tools → Macro → New** (veya Alt+F11)
3. Macro ismini girin: `Test` (örnek)
4. **Save** tıklayın
5. **VBA Editor penceresi** açılır

### Adım 2: Kodu Kopyalayın

1. Bu klasördeki **01_Temel_Giris.bas** dosyasını **metin editörü ile açın** (Notepad, VS Code, vb.)
2. **Tüm kodu seçin** (Ctrl+A)
3. **Kopyalayın** (Ctrl+C)

### Adım 3: VBA Editor'e Yapıştırın

1. VBA Editor penceresinde **Module1** çift tıklayın (sol panelde)
2. Sağ taraftaki **kod penceresine yapıştırın** (Ctrl+V)
3. **File → Save** (Ctrl+S)

### Adım 4: Çalıştırın

1. SolidWorks'te **bir parça açın** (File → Open)
2. VBA Editor'de istediğiniz fonksiyonu bulun (örn: `ParcaOzellikleri`)
3. İmleci fonksiyon içine getirin
4. **F5 tuşuna basın** (veya Run → Run Sub/UserForm)
5. Sonucu görün! 🎉

---

## 📋 YÖNTEM 2: Module Import (Alternatif)

### Adım 1: VBA Editor'ü Açın
1. SolidWorks → Tools → Macro → Edit
2. Herhangi bir macro seçin (veya yeni oluşturun)

### Adım 2: Module Import
1. VBA Editor'de **File → Import File**
2. **01_Temel_Giris.bas** dosyasını seçin
3. Sol panelde yeni bir Module eklenir

### Adım 3: Çalıştırın
1. Module'ü çift tıklayın
2. Fonksiyonu seçin
3. F5 ile çalıştırın

---

## ✅ İLK TESTİNİZ: "Merhaba Dünya"

Şimdi ilk VBA kodunuzu test edelim:

### Adım Adım:

**1. SolidWorks'ü açın**

**2. Tools → Macro → New**
   - İsim: `IlkTestim`
   - Kaydet

**3. VBA Editor açıldı. Şimdi bu basit kodu yapıştırın:**

```vba
Sub MerhabaDunya()
    Dim swApp As SldWorks.SldWorks
    Set swApp = Application.SldWorks

    MsgBox "Merhaba SolidWorks VBA Dunyasi!" & vbNewLine & _
           "SolidWorks Versiyonu: " & swApp.RevisionNumber(), _
           vbInformation, "Ilk VBA Programim"
End Sub
```

**4. F5 tuşuna basın**

**5. Mesaj kutusunu göreceksiniz!** ✅

---

## 🎯 ÖRNEK 1'İ TEST EDİN

Şimdi parça özellikleri örneğini deneyin:

### 1. Bir Parça Açın
- SolidWorks'te File → Open
- Herhangi bir .sldprt dosyası açın

### 2. Kodu Yapıştırın
- `01_Temel_Giris.bas` dosyasındaki **TÜM KODU** kopyalayın
- VBA Editor'de Module1'e yapıştırın

### 3. ParcaOzellikleri() Çalıştırın
```vba
' Kod içinde bu fonksiyonu bulun:
Sub ParcaOzellikleri()
    ' ... kod ...
End Sub
```

- İmleci `Sub ParcaOzellikleri()` satırına getirin
- **F5 tuşuna basın**
- Parçanın kütle, hacim bilgilerini görün! 🎉

---

## 🔧 SYNTAX ERROR ÇÖZÜMÜ

Eğer "Compile Error" veya "Syntax Error" alıyorsanız:

### Çözüm 1: SolidWorks API Referansını Ekleyin

1. VBA Editor'de **Tools → References**
2. Listede **"SolidWorks 20XX Type Library"** bulun (XX=sizin versiyonunuz)
3. **Checkbox'ı işaretleyin**
4. **OK** tıklayın

### Çözüm 2: Late Binding Kullanın

Eğer hala hata alıyorsanız, kod başındaki değişken tanımlarını değiştirin:

**Öncesi (Early Binding):**
```vba
Dim swApp As SldWorks.SldWorks
Dim swModel As SldWorks.ModelDoc2
```

**Sonrası (Late Binding):**
```vba
Dim swApp As Object
Dim swModel As Object

Set swApp = CreateObject("SldWorks.Application")
```

### Çözüm 3: Option Explicit'i Kaldırın (Geçici)

Kodun en başındaki bu satırı yoruma alın:

```vba
' Option Explicit  ' <- Başına apostrophe koyun
```

---

## 📝 ÖRNEK KODLAR HANGİSİ?

### Başlangıç: **01_Temel_Giris.bas**
- ✅ Merhaba Dünya
- ✅ Parça özellikleri
- ✅ Custom property işlemleri
- **Tavsiye:** Buradan başlayın!

### Orta: **02_Dosya_Islemleri.bas**
- ✅ Dosya açma/kaydetme
- ✅ STL/STEP export
- ✅ Toplu dönüştürme

### İleri: **03_STEP_To_STL_Montaj_Projesi.bas**
- ✅ Montaj için özel (1000+ parça)
- ✅ Toplu STEP+STL export
- **Önce basit örnekleri öğrenin!**

---

## 🐛 Sık Karşılaşılan Hatalar

### Hata: "ActiveX component can't create object"
**Çözüm:**
```vba
' Bunun yerine:
Set swApp = Application.SldWorks

' Bunu kullanın:
Set swApp = CreateObject("SldWorks.Application")
```

### Hata: "User-defined type not defined"
**Çözüm:** Tools → References → SolidWorks Type Library işaretleyin

### Hata: "Object variable not set"
**Çözüm:** `Set swApp = ...` satırını kontrol edin

### Hata: "Compile error: Invalid outside procedure"
**Çözüm:** Kod `Sub` ve `End Sub` arasında olmalı

---

## ✅ BAŞARI KONTROL LİSTESİ

Test edin ve işaretleyin:

- [ ] VBA Editor'ü açabildim
- [ ] Kodu kopyala-yapıştır yaptım
- [ ] `MerhabaDunya()` çalıştı
- [ ] Bir parça açtım
- [ ] `ParcaOzellikleri()` çalıştı ve sonuç gördüm
- [ ] SolidWorks API Reference ekledim

**Tümünü işaretlediyseniz → Hazırsınız! 🎉**

---

## 🆘 HALA SORUN MU VAR?

### Basit Debug Test:

VBA Editor'de yeni bir Module açın ve bu **en basit kodu** test edin:

```vba
Sub SimplestTest()
    MsgBox "VBA calisiyor!"
End Sub
```

- F5 ile çalıştırın
- Mesaj kutusunu görüyorsanız → VBA çalışıyor, SolidWorks API'yi eklemelisiniz
- Hata alıyorsanız → VBA kurulumunda sorun var

### Hangi SolidWorks Versiyonu?

Versiyonunuzu kontrol edin:
```vba
Sub VersionKontrol()
    MsgBox CreateObject("SldWorks.Application").RevisionNumber()
End Sub
```

---

## 📞 DESTEK

Sorunları bildirirken şunları belirtin:
1. Hangi örneği çalıştırdınız? (01, 02, 03?)
2. Tam hata mesajı nedir?
3. SolidWorks versiyonu nedir?
4. VBA Editor'de Tools → References'da hangileri işaretli?

---

## 🎯 SONRAKI ADIM

Başarılı test ettikten sonra:

1. **01_Temel_Giris.bas** → Tüm örnekleri deneyin (8 fonksiyon)
2. **02_Dosya_Islemleri.bas** → STL export test edin
3. **03_STEP_To_STL_Montaj_Projesi.bas** → Küçük montajda deneyin

**Kolay gelsin! VBA öğrenme yolculuğu başlasın! 🚀**
