' ================================================================
' SOLIDWORKS VBA ORNEKLERI - BASLANGIC SEVIYESI
' ================================================================
'
' Bu dosya SolidWorks VBA'ya giris icin hazirlanmistir.
' Dosya: solidworks_vba_ornekler/01_Temel_Giris.swp
'
' NASIL KULLANILIR:
' 1. SolidWorks'u acin
' 2. Tools > Macro > New
' 3. Bu kodu kopyalayin
' 4. F5 ile calistirin
'
' ================================================================

Option Explicit

' ================================================================
' ORNEK 1: Merhaba Dunya - SolidWorks Versiyonu
' ================================================================
Sub MerhabaDunya()
    Dim swApp As SldWorks.SldWorks

    ' SolidWorks uygulamasina baglan
    Set swApp = Application.SldWorks

    ' Mesaj kutusu goster
    MsgBox "Merhaba SolidWorks VBA Dunyasi!" & vbNewLine & _
           "SolidWorks Versiyonu: " & swApp.RevisionNumber(), _
           vbInformation, "Ilk VBA Programim"
End Sub


' ================================================================
' ORNEK 2: Acik Belge Bilgisi
' ================================================================
Sub AcikBelgeBilgisi()
    Dim swApp As SldWorks.SldWorks
    Dim swModel As SldWorks.ModelDoc2
    Dim modelAdi As String
    Dim modelTipi As String

    ' SolidWorks'e baglan
    Set swApp = Application.SldWorks

    ' Aktif belgeyi al
    Set swModel = swApp.ActiveDoc

    ' Belge acik mi kontrol et
    If swModel Is Nothing Then
        MsgBox "Hata: Once bir parca, montaj veya cizim acin!", vbExclamation
        Exit Sub
    End If

    ' Model adini al
    modelAdi = swModel.GetTitle()

    ' Model tipini belirle
    Select Case swModel.GetType()
        Case swDocPART
            modelTipi = "Parca"
        Case swDocASSEMBLY
            modelTipi = "Montaj"
        Case swDocDRAWING
            modelTipi = "Cizim"
        Case Else
            modelTipi = "Bilinmiyor"
    End Select

    ' Bilgileri goster
    MsgBox "Acik Belge Bilgileri:" & vbNewLine & vbNewLine & _
           "Dosya Adi: " & modelAdi & vbNewLine & _
           "Dosya Tipi: " & modelTipi, _
           vbInformation, "Belge Bilgisi"
End Sub


' ================================================================
' ORNEK 3: Parca Ozellikleri (Sadece PART dosyasi icin)
' ================================================================
Sub ParcaOzellikleri()
    Dim swApp As SldWorks.SldWorks
    Dim swModel As SldWorks.ModelDoc2
    Dim swPart As SldWorks.PartDoc
    Dim swMassProp As SldWorks.MassProperty
    Dim kutle As Double
    Dim hacim As Double
    Dim yuzeyAlani As Double
    Dim mesaj As String

    ' SolidWorks'e baglan
    Set swApp = Application.SldWorks
    Set swModel = swApp.ActiveDoc

    ' Belge kontrolu
    If swModel Is Nothing Then
        MsgBox "Hata: Once bir parca acin!", vbExclamation
        Exit Sub
    End If

    ' Parca mi kontrol et
    If swModel.GetType() <> swDocPART Then
        MsgBox "Hata: Bu makro sadece PARCA dosyalari icin calisir!", vbExclamation
        Exit Sub
    End If

    ' PartDoc'a cast et
    Set swPart = swModel

    ' Kutle ozellikleri al
    Set swMassProp = swModel.Extension.CreateMassProperty()

    If swMassProp Is Nothing Then
        MsgBox "Hata: Kutle ozellikleri alinamadi!", vbCritical
        Exit Sub
    End If

    ' Degerleri oku
    kutle = swMassProp.Mass ' kg
    hacim = swMassProp.Volume ' m^3
    yuzeyAlani = swMassProp.SurfaceArea ' m^2

    ' Mesaj olustur
    mesaj = "PARCA OZELLIKLERI" & vbNewLine & _
            String(50, "=") & vbNewLine & vbNewLine & _
            "Dosya: " & swModel.GetTitle() & vbNewLine & vbNewLine & _
            "Kutle: " & Format(kutle, "0.000") & " kg" & vbNewLine & _
            "Hacim: " & Format(hacim * 1000000000, "0.00") & " cm³" & vbNewLine & _
            "Yuzey Alani: " & Format(yuzeyAlani * 10000, "0.00") & " cm²"

    MsgBox mesaj, vbInformation, "Parca Bilgileri"
End Sub


' ================================================================
' ORNEK 4: Tum Acik Belgeleri Listele
' ================================================================
Sub AcikBelgeleriListele()
    Dim swApp As SldWorks.SldWorks
    Dim swModel As SldWorks.ModelDoc2
    Dim vModels As Variant
    Dim i As Integer
    Dim liste As String

    Set swApp = Application.SldWorks

    ' Acik belgeleri al
    vModels = swApp.GetDocuments

    If IsEmpty(vModels) Then
        MsgBox "Acik belge yok!", vbInformation
        Exit Sub
    End If

    ' Liste olustur
    liste = "ACIK BELGELER (" & UBound(vModels) + 1 & " adet)" & vbNewLine & _
            String(50, "=") & vbNewLine & vbNewLine

    For i = 0 To UBound(vModels)
        Set swModel = vModels(i)
        liste = liste & (i + 1) & ". " & swModel.GetTitle() & vbNewLine
    Next i

    MsgBox liste, vbInformation, "Acik Belgeler"
End Sub


' ================================================================
' ORNEK 5: Ozellik (Custom Property) Okuma
' ================================================================
Sub OzellikOku()
    Dim swApp As SldWorks.SldWorks
    Dim swModel As SldWorks.ModelDoc2
    Dim swCustProp As SldWorks.CustomPropertyManager
    Dim ozellikAdi As String
    Dim ozellikDegeri As String
    Dim ciktiDegeri As String
    Dim wasResolved As Boolean

    Set swApp = Application.SldWorks
    Set swModel = swApp.ActiveDoc

    If swModel Is Nothing Then
        MsgBox "Once bir belge acin!", vbExclamation
        Exit Sub
    End If

    ' Custom property manager'i al
    Set swCustProp = swModel.Extension.CustomPropertyManager("")

    ' "Description" ozelligini oku (ornek)
    ozellikAdi = "Description"
    swCustProp.Get4 ozellikAdi, wasResolved, ozellikDegeri, ciktiDegeri

    If ozellikDegeri = "" Then
        MsgBox "'" & ozellikAdi & "' ozelligi bulunamadi veya bos!", vbInformation
    Else
        MsgBox "Ozellik: " & ozellikAdi & vbNewLine & _
               "Deger: " & ozellikDegeri, vbInformation
    End If
End Sub


' ================================================================
' ORNEK 6: Ozellik (Custom Property) Yazma
' ================================================================
Sub OzellikYaz()
    Dim swApp As SldWorks.SldWorks
    Dim swModel As SldWorks.ModelDoc2
    Dim swCustProp As SldWorks.CustomPropertyManager
    Dim retVal As Long

    Set swApp = Application.SldWorks
    Set swModel = swApp.ActiveDoc

    If swModel Is Nothing Then
        MsgBox "Once bir belge acin!", vbExclamation
        Exit Sub
    End If

    ' Custom property manager'i al
    Set swCustProp = swModel.Extension.CustomPropertyManager("")

    ' Ozellik ekle/guncelle
    retVal = swCustProp.Add3("Olusturan", swCustomInfoText, "VBA Makro", swCustomPropertyOnlyIfNew)
    retVal = swCustProp.Add3("Tarih", swCustomInfoText, Date, swCustomPropertyOnlyIfNew)
    retVal = swCustProp.Add3("Versiyon", swCustomInfoText, "1.0", swCustomPropertyReplaceValue)

    MsgBox "Ozellikler eklendi/guncellendi!" & vbNewLine & vbNewLine & _
           "- Olusturan: VBA Makro" & vbNewLine & _
           "- Tarih: " & Date & vbNewLine & _
           "- Versiyon: 1.0", _
           vbInformation, "Basarili"
End Sub


' ================================================================
' ORNEK 7: Belge Kaydetme
' ================================================================
Sub BelgeKaydet()
    Dim swApp As SldWorks.SldWorks
    Dim swModel As SldWorks.ModelDoc2
    Dim errors As Long
    Dim warnings As Long
    Dim retVal As Boolean

    Set swApp = Application.SldWorks
    Set swModel = swApp.ActiveDoc

    If swModel Is Nothing Then
        MsgBox "Once bir belge acin!", vbExclamation
        Exit Sub
    End If

    ' Belgeyi kaydet
    retVal = swModel.Save3(swSaveAsOptions_Silent, errors, warnings)

    If retVal Then
        MsgBox "Belge basariyla kaydedildi!", vbInformation
    Else
        MsgBox "Hata: Belge kaydedilemedi!" & vbNewLine & _
               "Hata kodu: " & errors, vbCritical
    End If
End Sub


' ================================================================
' ORNEK 8: Ekran Yenilemesi Kontrolu (Performans icin)
' ================================================================
Sub EkranYenilemeOrnegi()
    Dim swApp As SldWorks.SldWorks
    Dim swModel As SldWorks.ModelDoc2
    Dim i As Integer

    Set swApp = Application.SldWorks
    Set swModel = swApp.ActiveDoc

    If swModel Is Nothing Then
        MsgBox "Once bir belge acin!", vbExclamation
        Exit Sub
    End If

    ' Ekran yenilemeyi kapat (hiz icin)
    swModel.FeatureManager.EnableFeatureTree = False
    swApp.Visible = True ' Arka planda calismaz (gorunur kalmali)

    ' Burada yogun islemler yapilabilir
    ' Ornek: 100 islem
    For i = 1 To 100
        ' Islem yap...
        DoEvents ' Windows mesajlarini isle
    Next i

    ' Ekran yenilemeyi ac
    swModel.FeatureManager.EnableFeatureTree = True
    swModel.ForceRebuild3 False ' Modeli yenile

    MsgBox "Islemler tamamlandi!", vbInformation
End Sub


' ================================================================
' YARDIMCI FONKSIYONLAR
' ================================================================

' Belge tipini string'e cevirir
Function BelgeTipiAl(tipKodu As Integer) As String
    Select Case tipKodu
        Case swDocPART: BelgeTipiAl = "Parca (.sldprt)"
        Case swDocASSEMBLY: BelgeTipiAl = "Montaj (.sldasm)"
        Case swDocDRAWING: BelgeTipiAl = "Cizim (.slddrw)"
        Case Else: BelgeTipiAl = "Bilinmiyor"
    End Select
End Function

' Dosya var mi kontrol et
Function DosyaVarMi(dosyaYolu As String) As Boolean
    Dim fso As Object
    Set fso = CreateObject("Scripting.FileSystemObject")
    DosyaVarMi = fso.FileExists(dosyaYolu)
End Function


' ================================================================
' NOTLAR VE IPUCLARI
' ================================================================
'
' 1. HATA AYIKLAMA:
'    - Debug.Print ile Immediate Window'a yaz
'    - F8 ile adim adim calistir
'    - Ctrl+G ile Immediate Window'u ac
'
' 2. YARDIM:
'    - F1 ile SolidWorks API Help
'    - api.solidworks.com adresinde dokumanlar
'
' 3. DEGISKEN TIPLERI:
'    - SldWorks.SldWorks = Ana uygulama
'    - SldWorks.ModelDoc2 = Genel belge (parca/montaj/cizim)
'    - SldWorks.PartDoc = Parca ozel
'    - SldWorks.AssemblyDoc = Montaj ozel
'
' 4. SIKCA KULLANILAN METODLAR:
'    - swApp.ActiveDoc - Aktif belgeyi al
'    - swModel.GetTitle() - Dosya adi
'    - swModel.GetPathName() - Tam dosya yolu
'    - swModel.Save3() - Kaydet
'    - swModel.ForceRebuild3() - Yeniden olustur
'
' 5. PERFORMANS:
'    - Ekran yenilemeyi kapat (EnableFeatureTree = False)
'    - Toplu islemlerde gorselestirmeyi kapat
'    - DoEvents ile Windows mesajlarini isle
'
' ================================================================
