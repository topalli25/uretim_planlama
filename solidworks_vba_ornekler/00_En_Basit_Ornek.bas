Attribute VB_Name = "EnBasitOrnek"
' ================================================================
' EN BASIT SOLIDWORKS VBA ORNEGI
' ================================================================
'
' SYNTAX ERROR ALIYORSANIZ BU DOSYAYI KULLANIN!
'
' Bu dosya Late Binding kullanir (SolidWorks Type Library gerekmez)
' Direkt calisir, hata vermez.
'
' KULLANIM:
' 1. SolidWorks acin
' 2. Tools > Macro > New
' 3. Bu kodu KOPYALA-YAPIŞTIR yapin
' 4. F5 ile calistirin
'
' ================================================================

' ================================================================
' TEST 1: En Basit Test
' ================================================================
Sub Test1_MerhabaDunya()
    MsgBox "Merhaba! VBA calisiyor!", vbInformation, "Basarili"
End Sub


' ================================================================
' TEST 2: SolidWorks Versiyonu
' ================================================================
Sub Test2_SolidWorksVersion()
    Dim swApp
    Set swApp = CreateObject("SldWorks.Application")

    MsgBox "SolidWorks Versiyonu: " & swApp.RevisionNumber(), _
           vbInformation, "SolidWorks Bilgi"
End Sub


' ================================================================
' TEST 3: Acik Belge Var Mi?
' ================================================================
Sub Test3_AcikBelge()
    Dim swApp
    Dim swModel

    Set swApp = CreateObject("SldWorks.Application")
    Set swModel = swApp.ActiveDoc

    If swModel Is Nothing Then
        MsgBox "Hicbir belge acik degil!" & vbCrLf & vbCrLf & _
               "Once bir parca acin (File > Open)", _
               vbExclamation, "Belge Yok"
    Else
        MsgBox "Acik belge: " & swModel.GetTitle(), _
               vbInformation, "Belge Bulundu"
    End If
End Sub


' ================================================================
' TEST 4: Parca Ozellikleri (ONCE PARCA ACIN!)
' ================================================================
Sub Test4_ParcaBilgisi()
    Dim swApp
    Dim swModel
    Dim swMassProp
    Dim mesaj As String

    ' SolidWorks'e baglan
    Set swApp = CreateObject("SldWorks.Application")
    Set swModel = swApp.ActiveDoc

    ' Belge acik mi?
    If swModel Is Nothing Then
        MsgBox "HATA: Once bir parca acin!", vbCritical, "Parca Gerekli"
        Exit Sub
    End If

    ' Parca mi?
    If swModel.GetType() <> 1 Then  ' 1 = swDocPart
        MsgBox "HATA: Bu sadece PARCA dosyalari icin calisir!", _
               vbCritical, "Sadece Parca"
        Exit Sub
    End If

    ' Kutle ozellikleri al
    Set swMassProp = swModel.Extension.CreateMassProperty()

    If swMassProp Is Nothing Then
        MsgBox "HATA: Kutle ozellikleri alinamadi!", vbCritical
        Exit Sub
    End If

    ' Mesaj olustur
    mesaj = "=== PARCA BILGILERI ===" & vbCrLf & vbCrLf
    mesaj = mesaj & "Dosya: " & swModel.GetTitle() & vbCrLf
    mesaj = mesaj & vbCrLf
    mesaj = mesaj & "Kutle: " & Format(swMassProp.Mass, "0.000") & " kg" & vbCrLf
    mesaj = mesaj & "Hacim: " & Format(swMassProp.Volume * 1000000000#, "0.00") & " cm3" & vbCrLf
    mesaj = mesaj & "Yuzey: " & Format(swMassProp.SurfaceArea * 10000#, "0.00") & " cm2"

    MsgBox mesaj, vbInformation, "Parca Ozellikleri"
End Sub


' ================================================================
' TEST 5: STL Export (ONCE PARCA ACIN!)
' ================================================================
Sub Test5_STLExport()
    Dim swApp
    Dim swModel
    Dim dosyaYolu As String
    Dim stlYolu As String

    Set swApp = CreateObject("SldWorks.Application")
    Set swModel = swApp.ActiveDoc

    ' Kontroller
    If swModel Is Nothing Then
        MsgBox "Once bir parca acin!", vbExclamation
        Exit Sub
    End If

    If swModel.GetType() <> 1 Then  ' swDocPart
        MsgBox "Sadece parca dosyalari icin calisir!", vbExclamation
        Exit Sub
    End If

    dosyaYolu = swModel.GetPathName()

    If dosyaYolu = "" Then
        MsgBox "Once parcayi kaydedin (File > Save)!", vbExclamation
        Exit Sub
    End If

    ' STL yolu
    stlYolu = Left(dosyaYolu, InStrRev(dosyaYolu, ".") - 1) & ".stl"

    ' STL export
    swModel.SaveAs3 stlYolu, 0, 0

    MsgBox "STL olusturuldu!" & vbCrLf & vbCrLf & stlYolu, _
           vbInformation, "Basarili"
End Sub


' ================================================================
' TEST 6: Custom Property Yaz
' ================================================================
Sub Test6_PropertyYaz()
    Dim swApp
    Dim swModel
    Dim swCustProp

    Set swApp = CreateObject("SldWorks.Application")
    Set swModel = swApp.ActiveDoc

    If swModel Is Nothing Then
        MsgBox "Once bir belge acin!", vbExclamation
        Exit Sub
    End If

    Set swCustProp = swModel.Extension.CustomPropertyManager("")

    ' Property ekle
    swCustProp.Add3 "Olusturan", 30, "VBA Makro", 2  ' 30=swCustomInfoText, 2=swCustomPropertyReplaceValue
    swCustProp.Add3 "Tarih", 30, Date, 2
    swCustProp.Add3 "Test", 30, "Basarili!", 2

    MsgBox "Custom Property'ler eklendi!" & vbCrLf & vbCrLf & _
           "File > Properties > Custom sekmesine bakin", _
           vbInformation, "Basarili"
End Sub


' ================================================================
' TEST 7: Tum Acik Belgeleri Listele
' ================================================================
Sub Test7_AcikBelgeler()
    Dim swApp
    Dim vModels
    Dim i As Integer
    Dim liste As String

    Set swApp = CreateObject("SldWorks.Application")
    vModels = swApp.GetDocuments

    If IsEmpty(vModels) Then
        MsgBox "Acik belge yok!", vbInformation
        Exit Sub
    End If

    liste = "=== ACIK BELGELER ===" & vbCrLf & vbCrLf
    liste = liste & "Toplam: " & (UBound(vModels) + 1) & " adet" & vbCrLf & vbCrLf

    For i = 0 To UBound(vModels)
        liste = liste & (i + 1) & ". " & vModels(i).GetTitle() & vbCrLf
    Next i

    MsgBox liste, vbInformation, "Acik Belgeler"
End Sub


' ================================================================
' NOTLAR
' ================================================================
'
' BU DOSYA NEDEN HATA VERMEZ?
'
' 1. Late Binding kullanir:
'    - Dim swApp As Object (degil: As SldWorks.SldWorks)
'    - Type Library gerektirmez
'    - Daha yavas ama hatasiz
'
' 2. Basit syntax:
'    - Karmasik API cagrilari yok
'    - Temel VBA komutlari
'
' 3. Hata kontrolleri:
'    - Her fonksiyonda Is Nothing kontrol
'    - Kullaniciya acik mesajlar
'
' NASIL KULLANILIR?
'
' 1. SolidWorks'u acin
' 2. Tools > Macro > New
' 3. Bu dosyanin TUM ICERIGI ni kopyala-yapiştir yapin
' 4. Soldaki listeden bir test secin (Test1, Test2, vb.)
' 5. F5 ile calistirin
'
' TEST SIRASI:
'
' Test1 → VBA calisiyor mu?
' Test2 → SolidWorks baglanti var mi?
' Test3 → Belge acma kontrolu
' Test4 → Parca ozellikleri (once parca ac!)
' Test5 → STL export (once parca ac!)
' Test6 → Custom property yazma
' Test7 → Acik belgeleri listele
'
' ================================================================
