' ================================================================
' SOLIDWORKS VBA ORNEKLERI - DOSYA ISLEMLERI
' ================================================================
'
' Bu dosya SolidWorks'te dosya acma, kaydetme, export islemleri icin
' hazirlanmistir.
'
' Dosya: solidworks_vba_ornekler/02_Dosya_Islemleri.swp
'
' ================================================================

Option Explicit

' ================================================================
' ORNEK 1: Parca Ac
' ================================================================
Sub ParcaAc()
    Dim swApp As SldWorks.SldWorks
    Dim swModel As SldWorks.ModelDoc2
    Dim dosyaYolu As String
    Dim errors As Long
    Dim warnings As Long

    Set swApp = Application.SldWorks

    ' Dosya yolu (BURAYA KENDI DOSYANIZIN YOLUNU YAZIN)
    dosyaYolu = "C:\Temp\test.sldprt"

    ' Dosya var mi kontrol et
    If Dir(dosyaYolu) = "" Then
        MsgBox "Hata: Dosya bulunamadi!" & vbNewLine & dosyaYolu, vbCritical
        Exit Sub
    End If

    ' Parcayi ac
    Set swModel = swApp.OpenDoc6(dosyaYolu, swDocPART, swOpenDocOptions_Silent, "", errors, warnings)

    If swModel Is Nothing Then
        MsgBox "Hata: Dosya acilamadi!" & vbNewLine & _
               "Hata kodu: " & errors, vbCritical
    Else
        MsgBox "Parca basariyla acildi!" & vbNewLine & swModel.GetTitle(), vbInformation
    End If
End Sub


' ================================================================
' ORNEK 2: Dosya Secici Dialog ile Parca Ac
' ================================================================
Sub DosyaSeciciIleParcaAc()
    Dim swApp As SldWorks.SldWorks
    Dim swModel As SldWorks.ModelDoc2
    Dim dosyaYolu As String
    Dim errors As Long
    Dim warnings As Long

    Set swApp = Application.SldWorks

    ' Dosya secim dialog'u goster
    dosyaYolu = swApp.GetOpenFileName( _
        "SolidWorks Parcasi Secin", _
        "", _
        "SolidWorks Parcalari (*.sldprt)|*.sldprt|Tum Dosyalar (*.*)|*.*|", _
        0, "", "")

    ' Kullanici iptal etti mi?
    If dosyaYolu = "" Then
        MsgBox "Islem iptal edildi.", vbInformation
        Exit Sub
    End If

    ' Dosyayi ac
    Set swModel = swApp.OpenDoc6(dosyaYolu, swDocPART, swOpenDocOptions_Silent, "", errors, warnings)

    If Not swModel Is Nothing Then
        MsgBox "Dosya acildi: " & swModel.GetTitle(), vbInformation
    Else
        MsgBox "Dosya acilamadi! Hata: " & errors, vbCritical
    End If
End Sub


' ================================================================
' ORNEK 3: STL Export
' ================================================================
Sub STLExport()
    Dim swApp As SldWorks.SldWorks
    Dim swModel As SldWorks.ModelDoc2
    Dim swPart As SldWorks.PartDoc
    Dim dosyaYolu As String
    Dim stlYolu As String
    Dim retVal As Boolean
    Dim errors As Long
    Dim warnings As Long

    Set swApp = Application.SldWorks
    Set swModel = swApp.ActiveDoc

    ' Belge kontrolu
    If swModel Is Nothing Then
        MsgBox "Hata: Once bir parca acin!", vbExclamation
        Exit Sub
    End If

    ' Parca mi?
    If swModel.GetType() <> swDocPART Then
        MsgBox "Hata: Bu makro sadece PARCA dosyalari icin calisir!", vbExclamation
        Exit Sub
    End If

    Set swPart = swModel

    ' Mevcut dosya yolunu al
    dosyaYolu = swModel.GetPathName()

    If dosyaYolu = "" Then
        MsgBox "Hata: Once dosyayi kaydedin!", vbExclamation
        Exit Sub
    End If

    ' STL yolu olustur (ayni klasor, .stl uzantisi)
    stlYolu = Left(dosyaYolu, InStrRev(dosyaYolu, ".") - 1) & ".stl"

    ' STL export ayarlari
    ' swSTLFormat_Binary = 0 (binary - daha kucuk dosya)
    ' swSTLFormat_ASCII = 1 (text - daha buyuk ama okunabilir)
    swPart.SaveAs3 stlYolu, 0, 0

    MsgBox "STL export basarili!" & vbNewLine & vbNewLine & _
           "Kayit yeri: " & vbNewLine & stlYolu, _
           vbInformation, "STL Export"
End Sub


' ================================================================
' ORNEK 4: STEP Export (AP214 Protokolu)
' ================================================================
Sub STEPExport()
    Dim swApp As SldWorks.SldWorks
    Dim swModel As SldWorks.ModelDoc2
    Dim dosyaYolu As String
    Dim stepYolu As String
    Dim retVal As Long

    Set swApp = Application.SldWorks
    Set swModel = swApp.ActiveDoc

    If swModel Is Nothing Then
        MsgBox "Once bir belge acin!", vbExclamation
        Exit Sub
    End If

    ' Dosya yolu
    dosyaYolu = swModel.GetPathName()
    If dosyaYolu = "" Then
        MsgBox "Once dosyayi kaydedin!", vbExclamation
        Exit Sub
    End If

    ' STEP yolu
    stepYolu = Left(dosyaYolu, InStrRev(dosyaYolu, ".") - 1) & ".step"

    ' STEP export ayarlari
    ' swSaveAsSTEP = 4
    retVal = swModel.SaveAs3(stepYolu, 0, 0)

    If retVal = swFileSaveError_None Then
        MsgBox "STEP export basarili!" & vbNewLine & stepYolu, vbInformation
    Else
        MsgBox "STEP export basarisiz! Hata: " & retVal, vbCritical
    End If
End Sub


' ================================================================
' ORNEK 5: Farkli Isimle Kaydet
' ================================================================
Sub FarkliIsimleKaydet()
    Dim swApp As SldWorks.SldWorks
    Dim swModel As SldWorks.ModelDoc2
    Dim eskiYol As String
    Dim yeniYol As String
    Dim errors As Long
    Dim warnings As Long
    Dim retVal As Boolean

    Set swApp = Application.SldWorks
    Set swModel = swApp.ActiveDoc

    If swModel Is Nothing Then
        MsgBox "Once bir belge acin!", vbExclamation
        Exit Sub
    End If

    eskiYol = swModel.GetPathName()

    ' Kayit dialogu goster
    yeniYol = swApp.GetSaveAsFilename( _
        "Farkli Kaydet", _
        "SolidWorks Parcalari (*.sldprt)|*.sldprt||", _
        0, "", "")

    If yeniYol = "" Then
        MsgBox "Islem iptal edildi.", vbInformation
        Exit Sub
    End If

    ' Kaydet
    retVal = swModel.Extension.SaveAs(yeniYol, swSaveAsVersion_CurrentVersion, _
                                       swSaveAsOptions_Silent, Nothing, errors, warnings)

    If retVal Then
        MsgBox "Dosya kaydedildi: " & vbNewLine & yeniYol, vbInformation
    Else
        MsgBox "Kaydetme hatasi! Kod: " & errors, vbCritical
    End If
End Sub


' ================================================================
' ORNEK 6: Klasordeki Tum Parcalari Ac ve STL Export Et
' ================================================================
Sub KlasordekiParcalariSTLYap()
    Dim swApp As SldWorks.SldWorks
    Dim swModel As SldWorks.ModelDoc2
    Dim fso As Object
    Dim klasor As Object
    Dim dosya As Object
    Dim klasorYolu As String
    Dim dosyaYolu As String
    Dim stlYolu As String
    Dim errors As Long
    Dim warnings As Long
    Dim sayac As Integer

    Set swApp = Application.SldWorks
    Set fso = CreateObject("Scripting.FileSystemObject")

    ' Klasor sec (BURAYA KLASOR YOLU YAZIN)
    klasorYolu = "C:\Temp\Parcalar\"

    ' Klasor var mi?
    If Not fso.FolderExists(klasorYolu) Then
        MsgBox "Klasor bulunamadi: " & klasorYolu, vbCritical
        Exit Sub
    End If

    Set klasor = fso.GetFolder(klasorYolu)
    sayac = 0

    ' Klasordeki her dosya icin
    For Each dosya In klasor.Files
        ' .sldprt dosyalari icin
        If LCase(fso.GetExtensionName(dosya.Path)) = "sldprt" Then

            dosyaYolu = dosya.Path
            stlYolu = Left(dosyaYolu, InStrRev(dosyaYolu, ".") - 1) & ".stl"

            ' Parcayi ac
            Set swModel = swApp.OpenDoc6(dosyaYolu, swDocPART, swOpenDocOptions_Silent, "", errors, warnings)

            If Not swModel Is Nothing Then
                ' STL export et
                swModel.SaveAs3 stlYolu, 0, 0

                ' Kapat
                swApp.CloseDoc swModel.GetTitle()

                sayac = sayac + 1
            End If
        End If
    Next dosya

    MsgBox "Tamamlandi!" & vbNewLine & _
           sayac & " parca STL'ye donusturuldu.", _
           vbInformation, "Toplu STL Export"
End Sub


' ================================================================
' ORNEK 7: PDF Export (Cizim icin)
' ================================================================
Sub PDFExport()
    Dim swApp As SldWorks.SldWorks
    Dim swModel As SldWorks.ModelDoc2
    Dim swDraw As SldWorks.DrawingDoc
    Dim dosyaYolu As String
    Dim pdfYolu As String
    Dim errors As Long
    Dim warnings As Long
    Dim retVal As Boolean

    Set swApp = Application.SldWorks
    Set swModel = swApp.ActiveDoc

    If swModel Is Nothing Then
        MsgBox "Once bir cizim acin!", vbExclamation
        Exit Sub
    End If

    If swModel.GetType() <> swDocDRAWING Then
        MsgBox "Bu makro sadece CIZIM dosyalari icin calisir!", vbExclamation
        Exit Sub
    End If

    Set swDraw = swModel

    dosyaYolu = swModel.GetPathName()
    If dosyaYolu = "" Then
        MsgBox "Once dosyayi kaydedin!", vbExclamation
        Exit Sub
    End If

    pdfYolu = Left(dosyaYolu, InStrRev(dosyaYolu, ".") - 1) & ".pdf"

    ' PDF export
    retVal = swModel.Extension.SaveAs(pdfYolu, swSaveAsVersion_CurrentVersion, _
                                       swSaveAsOptions_Silent, Nothing, errors, warnings)

    If retVal Then
        MsgBox "PDF olusturuldu: " & vbNewLine & pdfYolu, vbInformation
    Else
        MsgBox "PDF olusturulamadi! Hata: " & errors, vbCritical
    End If
End Sub


' ================================================================
' ORNEK 8: DXF/DWG Export (Cizim icin)
' ================================================================
Sub DXFExport()
    Dim swApp As SldWorks.SldWorks
    Dim swModel As SldWorks.ModelDoc2
    Dim dosyaYolu As String
    Dim dxfYolu As String
    Dim retVal As Boolean

    Set swApp = Application.SldWorks
    Set swModel = swApp.ActiveDoc

    If swModel Is Nothing Then
        MsgBox "Once bir cizim acin!", vbExclamation
        Exit Sub
    End If

    dosyaYolu = swModel.GetPathName()
    If dosyaYolu = "" Then
        MsgBox "Once dosyayi kaydedin!", vbExclamation
        Exit Sub
    End If

    dxfYolu = Left(dosyaYolu, InStrRev(dosyaYolu, ".") - 1) & ".dxf"

    ' DXF export
    retVal = swModel.SaveAs3(dxfYolu, 0, 0)

    If retVal Then
        MsgBox "DXF olusturuldu: " & vbNewLine & dxfYolu, vbInformation
    Else
        MsgBox "DXF olusturulamadi!", vbCritical
    End If
End Sub


' ================================================================
' ORNEK 9: Dosya Bilgisi Raporlama
' ================================================================
Sub DosyaBilgisiRapor()
    Dim swApp As SldWorks.SldWorks
    Dim swModel As SldWorks.ModelDoc2
    Dim fso As Object
    Dim dosya As Object
    Dim rapor As String

    Set swApp = Application.SldWorks
    Set swModel = swApp.ActiveDoc

    If swModel Is Nothing Then
        MsgBox "Once bir belge acin!", vbExclamation
        Exit Sub
    End If

    Set fso = CreateObject("Scripting.FileSystemObject")
    Set dosya = fso.GetFile(swModel.GetPathName())

    rapor = "DOSYA BILGISI RAPORU" & vbNewLine & _
            String(50, "=") & vbNewLine & vbNewLine & _
            "Dosya Adi: " & swModel.GetTitle() & vbNewLine & _
            "Tam Yol: " & swModel.GetPathName() & vbNewLine & _
            "Boyut: " & Format(dosya.Size / 1024, "0.00") & " KB" & vbNewLine & _
            "Olusturma: " & dosya.DateCreated & vbNewLine & _
            "Degistirme: " & dosya.DateLastModified & vbNewLine & _
            "Tip: " & BelgeTipiAl(swModel.GetType())

    MsgBox rapor, vbInformation, "Dosya Bilgisi"
End Sub


' ================================================================
' YARDIMCI FONKSIYONLAR
' ================================================================

Function BelgeTipiAl(tipKodu As Integer) As String
    Select Case tipKodu
        Case swDocPART: BelgeTipiAl = "Parca (.sldprt)"
        Case swDocASSEMBLY: BelgeTipiAl = "Montaj (.sldasm)"
        Case swDocDRAWING: BelgeTipiAl = "Cizim (.slddrw)"
        Case Else: BelgeTipiAl = "Bilinmiyor"
    End Select
End Function


' ================================================================
' NOTLAR
' ================================================================
'
' EXPORT FORMATLARI:
'
' STL (Mesh):
'   - Binary: Kucuk dosya, hizli
'   - ASCII: Buyuk dosya, okunabilir
'   - Kullanim: 3D printing, mesh islemleri
'
' STEP (CAD):
'   - AP203: Genel mekanik tasarim
'   - AP214: Otomotiv (renk ve katman bilgisi)
'   - Kullanim: CAD program arasi veri aktarimi
'
' PDF:
'   - Sadece Drawing dosyalari icin
'   - Evrensel goruntuleme
'
' DXF/DWG:
'   - 2D CAD cizimler
'   - AutoCAD uyumlu
'
' ================================================================
'
' PERFORMANS IPUCLARI:
'
' 1. Toplu islemlerde ekran guncellemeyi kapat
' 2. swOpenDocOptions_Silent kullan (dialog'siz ac)
' 3. Gereksiz rebuild yapmaktan kacin
' 4. Dosya yollarini degiskenlerde tut
' 5. Hata kontrolu yap (If Not Nothing Then...)
'
' ================================================================
