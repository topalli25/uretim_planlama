' ================================================================
' SOLIDWORKS VBA - MONTAJ KILAVUZU PROJESI
' ================================================================
'
' STEP to STL Toplu Donusturucu
' Montaj kilavuzu uygulamasi icin ozel hazirlanmistir.
'
' AMAC:
' - Montajdaki tum parcalari ayri ayri STEP olarak export et
' - Her STEP'i STL'ye donustur
' - JSON Creator ile kullanilmak uzere hazirla
'
' Dosya: solidworks_vba_ornekler/03_STEP_To_STL_Montaj_Projesi.swp
'
' ================================================================

Option Explicit

' Global degiskenler
Dim swApp As SldWorks.SldWorks
Dim ciktiKlasoru As String
Dim toplamParca As Integer
Dim basariliSTEP As Integer
Dim basariliSTL As Integer
Dim basarisizlar As Integer


' ================================================================
' ANA FONKSIYON: Montaji STEP + STL'ye Donustur
' ================================================================
Sub MontajdanSTEPveSTLOlustur()
    Dim swModel As SldWorks.ModelDoc2
    Dim swAssy As SldWorks.AssemblyDoc
    Dim baslamaZamani As Double
    Dim bitisZamani As Double
    Dim gecenSure As Double

    ' Baslangic
    baslamaZamani = Timer
    basariliSTEP = 0
    basariliSTL = 0
    basarisizlar = 0
    toplamParca = 0

    ' SolidWorks'e baglan
    Set swApp = Application.SldWorks
    Set swModel = swApp.ActiveDoc

    ' Montaj kontrolu
    If swModel Is Nothing Then
        MsgBox "Hata: Once bir MONTAJ dosyasi acin!", vbExclamation, "Montaj Gerekli"
        Exit Sub
    End If

    If swModel.GetType() <> swDocASSEMBLY Then
        MsgBox "Hata: Bu makro sadece MONTAJ dosyalari icin calisir!", _
               vbExclamation, "Sadece Montaj"
        Exit Sub
    End If

    Set swAssy = swModel

    ' Cikti klasoru sec
    ciktiKlasoru = SecKlasor("STEP ve STL dosyalari icin cikti klasoru secin:")

    If ciktiKlasoru = "" Then
        MsgBox "Islem iptal edildi.", vbInformation
        Exit Sub
    End If

    ' STEP export parametrelerini ayarla
    Call STEPAyarlariYap

    ' Ana islem baslat
    MsgBox "Montaj export islemi baslayacak..." & vbNewLine & vbNewLine & _
           "Montaj: " & swModel.GetTitle() & vbNewLine & _
           "Cikti: " & ciktiKlasoru & vbNewLine & vbNewLine & _
           "Bu islem birka dakika surebilir.", _
           vbInformation, "Baslayalim"

    ' Ekran guncellemeyi kapat (performans)
    swApp.Visible = True
    swModel.FeatureManager.EnableFeatureTree = False

    ' Parcalari isle
    Call MontajParcalariniIsle(swAssy)

    ' Ekrani aktif et
    swModel.FeatureManager.EnableFeatureTree = True
    swModel.ForceRebuild3 False

    ' Bitis
    bitisZamani = Timer
    gecenSure = bitisZamani - baslamaZamani

    ' Sonuc raporu
    MsgBox "TAMAMLANDI!" & vbNewLine & _
           String(50, "=") & vbNewLine & vbNewLine & _
           "Toplam Parca: " & toplamParca & vbNewLine & _
           "STEP Export: " & basariliSTEP & vbNewLine & _
           "STL Donusum: " & basariliSTL & vbNewLine & _
           "Basarisiz: " & basarisizlar & vbNewLine & vbNewLine & _
           "Gecen Sure: " & Format(gecenSure, "0.0") & " saniye" & vbNewLine & _
           "Cikti Klasoru: " & vbNewLine & ciktiKlasoru, _
           vbInformation, "Export Tamamlandi"

    ' Log dosyasi olustur
    Call LogDosyasiOlustur(gecenSure)

End Sub


' ================================================================
' Montaj Parcalarini Isle ve Export Et
' ================================================================
Sub MontajParcalariniIsle(swAssy As SldWorks.AssemblyDoc)
    Dim vComps As Variant
    Dim swComp As SldWorks.Component2
    Dim swCompModel As SldWorks.ModelDoc2
    Dim i As Integer
    Dim parcaAdi As String
    Dim stepDosya As String
    Dim stlDosya As String

    ' Montajdaki tum componentleri al
    vComps = swAssy.GetComponents(False)

    If IsEmpty(vComps) Then
        MsgBox "Montajda parca bulunamadi!", vbExclamation
        Exit Sub
    End If

    toplamParca = UBound(vComps) + 1

    ' Her component icin
    For i = 0 To UBound(vComps)
        Set swComp = vComps(i)

        ' Component visible ve suppressed degil mi?
        If swComp.Visible = swComponentVisible And _
           swComp.IsSuppressed() = False Then

            ' Component model'i al
            Set swCompModel = swComp.GetModelDoc2()

            If Not swCompModel Is Nothing Then
                ' Sadece part'lar icin (sub-assembly'ler atlanir)
                If swCompModel.GetType() = swDocPART Then

                    ' Parca adi (benzersiz yap)
                    parcaAdi = TemizParcaAdi(swComp.Name2)
                    parcaAdi = parcaAdi & "_" & Format(i + 1, "000")

                    ' Dosya yollari
                    stepDosya = ciktiKlasoru & "\" & parcaAdi & ".step"
                    stlDosya = ciktiKlasoru & "\" & parcaAdi & ".stl"

                    ' STEP export et
                    If STEPExportEt(swCompModel, stepDosya) Then
                        basariliSTEP = basariliSTEP + 1

                        ' STL'ye donustur
                        If STLDonustur(stepDosya, stlDosya) Then
                            basariliSTL = basariliSTL + 1
                        Else
                            basarisizlar = basarisizlar + 1
                        End If
                    Else
                        basarisizlar = basarisizlar + 1
                    End If

                    ' İlerleme goster (her 10 parcada bir)
                    If (i + 1) Mod 10 = 0 Then
                        swApp.SendMsgToUser2 "Isleniyor: " & (i + 1) & " / " & toplamParca, _
                                            swMessageBoxIcon_e.swMbInformation, _
                                            swMessageBoxBtn_e.swMbOk
                        DoEvents
                    End If
                End If
            End If
        End If
    Next i
End Sub


' ================================================================
' STEP Export Et
' ================================================================
Function STEPExportEt(swModel As SldWorks.ModelDoc2, stepDosya As String) As Boolean
    Dim retVal As Long
    Dim errors As Long
    Dim warnings As Long

    On Error GoTo ErrorHandler

    ' STEP olarak kaydet
    retVal = swModel.Extension.SaveAs(stepDosya, _
                                       swSaveAsVersion_CurrentVersion, _
                                       swSaveAsOptions_Silent, _
                                       Nothing, errors, warnings)

    If retVal And errors = 0 Then
        STEPExportEt = True
    Else
        STEPExportEt = False
        Debug.Print "STEP export hatasi: " & stepDosya & " (Hata: " & errors & ")"
    End If

    Exit Function

ErrorHandler:
    STEPExportEt = False
    Debug.Print "STEP export exception: " & Err.Description
End Function


' ================================================================
' STL'ye Donustur
' ================================================================
Function STLDonustur(stepDosya As String, stlDosya As String) As Boolean
    Dim swModel As SldWorks.ModelDoc2
    Dim errors As Long
    Dim warnings As Long
    Dim retVal As Boolean

    On Error GoTo ErrorHandler

    ' STEP dosyasini ac
    Set swModel = swApp.OpenDoc6(stepDosya, swDocPART, _
                                 swOpenDocOptions_Silent, "", errors, warnings)

    If swModel Is Nothing Then
        STLDonustur = False
        Debug.Print "STEP acilamadi: " & stepDosya
        Exit Function
    End If

    ' STL olarak kaydet
    retVal = swModel.Extension.SaveAs(stlDosya, _
                                       swSaveAsVersion_CurrentVersion, _
                                       swSaveAsOptions_Silent, _
                                       Nothing, errors, warnings)

    ' Dosyayi kapat
    swApp.CloseDoc swModel.GetTitle()

    STLDonustur = retVal

    Exit Function

ErrorHandler:
    STLDonustur = False
    Debug.Print "STL donusum exception: " & Err.Description
End Function


' ================================================================
' STEP Export Ayarlarini Yap
' ================================================================
Sub STEPAyarlariYap()
    ' STEP export ayarlarini optimize et
    ' AP214 protokolu (renk ve katman bilgisi)

    swApp.SetUserPreferenceIntegerValue swSTEPFormat, swSTEPFormat_AP214
    swApp.SetUserPreferenceToggle swSTEPExportSurfacesAs, True
    swApp.SetUserPreferenceToggle swSTEPExportPriorToSave, False
End Sub


' ================================================================
' Klasor Sec Dialog
' ================================================================
Function SecKlasor(mesaj As String) As String
    Dim shell As Object
    Dim klasor As Object

    Set shell = CreateObject("Shell.Application")
    Set klasor = shell.BrowseForFolder(0, mesaj, 0, 0)

    If Not klasor Is Nothing Then
        SecKlasor = klasor.Self.Path
    Else
        SecKlasor = ""
    End If
End Function


' ================================================================
' Parca Adini Temizle (gecersiz karakterleri kaldir)
' ================================================================
Function TemizParcaAdi(parcaAdi As String) As String
    Dim sonuc As String
    Dim i As Integer
    Dim karakter As String

    sonuc = parcaAdi

    ' Component instance numarasini kaldir (-1, -2, vb.)
    If InStr(sonuc, "-") > 0 Then
        sonuc = Left(sonuc, InStr(sonuc, "-") - 1)
    End If

    ' Dosya adi icin gecersiz karakterleri kaldir
    sonuc = Replace(sonuc, "/", "_")
    sonuc = Replace(sonuc, "\", "_")
    sonuc = Replace(sonuc, ":", "_")
    sonuc = Replace(sonuc, "*", "_")
    sonuc = Replace(sonuc, "?", "_")
    sonuc = Replace(sonuc, """", "_")
    sonuc = Replace(sonuc, "<", "_")
    sonuc = Replace(sonuc, ">", "_")
    sonuc = Replace(sonuc, "|", "_")
    sonuc = Replace(sonuc, " ", "_")

    TemizParcaAdi = sonuc
End Function


' ================================================================
' Log Dosyasi Olustur
' ================================================================
Sub LogDosyasiOlustur(gecenSure As Double)
    Dim fso As Object
    Dim logDosya As Object
    Dim logYol As String

    Set fso = CreateObject("Scripting.FileSystemObject")

    logYol = ciktiKlasoru & "\export_log.txt"

    Set logDosya = fso.CreateTextFile(logYol, True)

    logDosya.WriteLine "SOLIDWORKS MONTAJ EXPORT RAPORU"
    logDosya.WriteLine String(50, "=")
    logDosya.WriteLine ""
    logDosya.WriteLine "Tarih: " & Now
    logDosya.WriteLine "Montaj: " & swApp.ActiveDoc.GetTitle()
    logDosya.WriteLine "Cikti Klasoru: " & ciktiKlasoru
    logDosya.WriteLine ""
    logDosya.WriteLine "SONUCLAR:"
    logDosya.WriteLine "  Toplam Parca: " & toplamParca
    logDosya.WriteLine "  STEP Export: " & basariliSTEP
    logDosya.WriteLine "  STL Donusum: " & basariliSTL
    logDosya.WriteLine "  Basarisiz: " & basarisizlar
    logDosya.WriteLine ""
    logDosya.WriteLine "Gecen Sure: " & Format(gecenSure, "0.00") & " saniye"
    logDosya.WriteLine "Basari Orani: " & Format((basariliSTL / toplamParca) * 100, "0.0") & "%"

    logDosya.Close

    Debug.Print "Log dosyasi olusturuldu: " & logYol
End Sub


' ================================================================
' ALTERNATIF: Sadece STL Export (STEP Atla)
' ================================================================
Sub DogrudenSTLExport()
    ' Eger STEP gerektirmiyorsaniz, dogrudan STL export daha hizli olur

    Dim swModel As SldWorks.ModelDoc2
    Dim swAssy As SldWorks.AssemblyDoc
    Dim vComps As Variant
    Dim swComp As SldWorks.Component2
    Dim swCompModel As SldWorks.ModelDoc2
    Dim i As Integer
    Dim stlDosya As String
    Dim parcaAdi As String
    Dim sayac As Integer

    Set swApp = Application.SldWorks
    Set swModel = swApp.ActiveDoc

    If swModel Is Nothing Or swModel.GetType() <> swDocASSEMBLY Then
        MsgBox "Montaj acin!", vbExclamation
        Exit Sub
    End If

    Set swAssy = swModel

    ciktiKlasoru = SecKlasor("STL cikti klasoru:")
    If ciktiKlasoru = "" Then Exit Sub

    vComps = swAssy.GetComponents(False)
    sayac = 0

    For i = 0 To UBound(vComps)
        Set swComp = vComps(i)
        Set swCompModel = swComp.GetModelDoc2()

        If Not swCompModel Is Nothing Then
            If swCompModel.GetType() = swDocPART Then
                parcaAdi = TemizParcaAdi(swComp.Name2) & "_" & Format(i + 1, "000")
                stlDosya = ciktiKlasoru & "\" & parcaAdi & ".stl"

                ' Direkt STL export
                swCompModel.Extension.SaveAs stlDosya, swSaveAsVersion_CurrentVersion, _
                                              swSaveAsOptions_Silent, Nothing, 0, 0
                sayac = sayac + 1
            End If
        End If
    Next i

    MsgBox "Tamamlandi! " & sayac & " STL dosyasi olusturuldu.", vbInformation
End Sub


' ================================================================
' YARDIMCI: Parca Listesi Olustur (JSON Creator icin)
' ================================================================
Sub ParcaListesiOlustur()
    ' Montajdaki parcalarin listesini metin dosyasina yaz
    ' JSON Creator'da referans olarak kullanilabilir

    Dim swModel As SldWorks.ModelDoc2
    Dim swAssy As SldWorks.AssemblyDoc
    Dim vComps As Variant
    Dim swComp As SldWorks.Component2
    Dim fso As Object
    Dim listeDosya As Object
    Dim listeYol As String
    Dim i As Integer

    Set swApp = Application.SldWorks
    Set swModel = swApp.ActiveDoc

    If swModel Is Nothing Or swModel.GetType() <> swDocASSEMBLY Then
        MsgBox "Montaj acin!", vbExclamation
        Exit Sub
    End If

    Set swAssy = swModel
    Set fso = CreateObject("Scripting.FileSystemObject")

    listeYol = swModel.GetPathName()
    listeYol = Left(listeYol, InStrRev(listeYol, "\")) & "parca_listesi.txt"

    Set listeDosya = fso.CreateTextFile(listeYol, True)

    listeDosya.WriteLine "MONTAJ PARCA LISTESI"
    listeDosya.WriteLine "Montaj: " & swModel.GetTitle()
    listeDosya.WriteLine "Tarih: " & Now
    listeDosya.WriteLine String(70, "=")
    listeDosya.WriteLine ""

    vComps = swAssy.GetComponents(False)

    For i = 0 To UBound(vComps)
        Set swComp = vComps(i)
        listeDosya.WriteLine (i + 1) & ". " & swComp.Name2 & _
                             " (" & swComp.GetPathName() & ")"
    Next i

    listeDosya.Close

    MsgBox "Parca listesi olusturuldu:" & vbNewLine & listeYol, vbInformation
End Sub


' ================================================================
' NOTLAR VE KULLANIM
' ================================================================
'
' KULLANIM ADIMLARI:
'
' 1. SolidWorks'te montajinizi acin
' 2. Tools > Macro > Edit > Bu dosyayi secin
' 3. F5 veya Run > MontajdanSTEPveSTLOlustur
' 4. Cikti klasoru secin
' 5. Bekleyin (1000 parca ~10-20 dakika)
' 6. Cikti klasorunde STEP ve STL dosyalari hazir
'
' CIKTI:
' - Her parca icin .step dosyasi
' - Her parca icin .stl dosyasi
' - export_log.txt (rapor)
' - parca_listesi.txt (referans)
'
' JSON CREATOR ILE KULLANIM:
' 1. Bu VBA ile STEP+STL export yapin
' 2. JSON Creator'i acin
' 3. Cikti klasorunu secin
' 4. STL dosyalari otomatik yuklenir
' 5. Montaj adimlarini olusturun
' 6. JSON export edin
'
' PERFORMANS:
' - 100 parca: ~2-3 dakika
' - 500 parca: ~10-15 dakika
' - 1000 parca: ~20-30 dakika
'
' IPUCLARI:
' - Montajda suppressed parcalar atlanir
' - Sub-assembly'ler degilsadece part'lar export edilir
' - Dosya adlari otomatik temizlenir (gecersiz karakterler)
' - Her 10 parcada ilerleme mesaji gosterilir
'
' ================================================================
