"""
Ana uygulama penceresi
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                             QMenuBar, QMenu, QFileDialog, QMessageBox,
                             QStatusBar, QSplitter)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

from src.gui.gorunum_widget import GorunumWidget
from src.gui.kontrol_paneli import KontrolPaneli
from src.core.model_yukleyici import ModelYukleyici
from src.core.montaj_yoneticisi import MontajYoneticisi
from src.core.adim_yoneticisi import AdimYoneticisi
from src.utils.yardimcilar import konfig_al, proje_kok_dizini_al


class AnaPencere(QMainWindow):
    """Ana uygulama penceresi"""

    def __init__(self):
        super().__init__()

        # Config yükle
        self.konfig = konfig_al()

        # Modüller
        self.model_yukleyici = ModelYukleyici()
        self.montaj_yoneticisi = MontajYoneticisi()
        self.adim_yoneticisi = AdimYoneticisi()
        self.yuklenmis_modeller = {}  # parca_id: mesh

        # UI oluştur
        self.arayuzu_olustur()

    def arayuzu_olustur(self):
        """UI elemanlarını oluştur"""
        self.setWindowTitle(self.konfig['app']['name'])
        self.setGeometry(100, 100,
                        self.konfig['app']['window_width'],
                        self.konfig['app']['window_height'])

        # Merkezi widget
        merkezi_widget = QWidget()
        self.setCentralWidget(merkezi_widget)

        # Ana layout
        ana_layout = QHBoxLayout(merkezi_widget)

        # Splitter (3D viewer ve kontrol paneli)
        bolme = QSplitter(Qt.Orientation.Horizontal)

        # 3D Viewer
        self.gorunum = GorunumWidget()
        bolme.addWidget(self.gorunum)

        # Kontrol Paneli
        self.kontrol_paneli = KontrolPaneli()
        self.kontrol_paneli.setMaximumWidth(400)
        self.kontrol_paneli.setMinimumWidth(300)
        self.kontrol_paneli.adim_degisti.connect(self.adim_degisti_slot)
        self.kontrol_paneli.parca_secildi.connect(self.parca_secildi_slot)
        bolme.addWidget(self.kontrol_paneli)

        # Splitter oranı (70% viewer, 30% panel)
        bolme.setStretchFactor(0, 7)
        bolme.setStretchFactor(1, 3)

        ana_layout.addWidget(bolme)

        # Menü bar
        self.menu_cubugunu_olustur()

        # Status bar
        self.durum_cubugu = QStatusBar()
        self.setStatusBar(self.durum_cubugu)
        self.durum_cubugu.showMessage("Hazır")

    def menu_cubugunu_olustur(self):
        """Menü çubuğunu oluştur"""
        menubar = self.menuBar()

        # Dosya menüsü
        dosya_menusu = menubar.addMenu("Dosya")

        ac_aksiyonu = QAction("Montaj Aç...", self)
        ac_aksiyonu.setShortcut("Ctrl+O")
        ac_aksiyonu.triggered.connect(self.montaj_ac)
        dosya_menusu.addAction(ac_aksiyonu)

        dosya_menusu.addSeparator()

        cikis_aksiyonu = QAction("Çıkış", self)
        cikis_aksiyonu.setShortcut("Ctrl+Q")
        cikis_aksiyonu.triggered.connect(self.close)
        dosya_menusu.addAction(cikis_aksiyonu)

        # Görünüm menüsü
        gorunum_menusu = menubar.addMenu("Görünüm")

        kamera_sifirla_aksiyonu = QAction("Kamerayı Sıfırla", self)
        kamera_sifirla_aksiyonu.setShortcut("R")
        kamera_sifirla_aksiyonu.triggered.connect(self.gorunum.kamerayi_sifirla)
        gorunum_menusu.addAction(kamera_sifirla_aksiyonu)

        tam_ekran_aksiyonu = QAction("Tam Ekran", self)
        tam_ekran_aksiyonu.setShortcut("F11")
        tam_ekran_aksiyonu.setCheckable(True)
        tam_ekran_aksiyonu.triggered.connect(self.tam_ekran_degistir)
        gorunum_menusu.addAction(tam_ekran_aksiyonu)

        # Yardım menüsü
        yardim_menusu = menubar.addMenu("Yardım")

        hakkinda_aksiyonu = QAction("Hakkında", self)
        hakkinda_aksiyonu.triggered.connect(self.hakkinda_goster)
        yardim_menusu.addAction(hakkinda_aksiyonu)

    def montaj_ac(self):
        """Montaj dosyası aç"""
        proje_koku = proje_kok_dizini_al()
        montaj_dizini = proje_koku / self.konfig['paths']['assemblies_dir']

        dosya_yolu, _ = QFileDialog.getOpenFileName(
            self,
            "Montaj Dosyası Seç",
            str(montaj_dizini),
            "JSON Dosyaları (*.json)"
        )

        if dosya_yolu:
            try:
                self.montaj_yukle(dosya_yolu)
                self.durum_cubugu.showMessage(f"Montaj yüklendi: {dosya_yolu}")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Montaj yüklenemedi:\n{str(e)}")

    def montaj_yukle(self, montaj_dosyasi):
        """
        Montaj dosyasını yükle ve görselleştir

        Args:
            montaj_dosyasi (str): Montaj JSON dosyasının yolu
        """
        # Montaj bilgilerini yükle
        montaj_verisi = self.montaj_yoneticisi.montaj_yukle(montaj_dosyasi)

        # Adımları yükle
        self.adim_yoneticisi.adimlari_yukle(montaj_verisi.get('adimlar', []))

        # 3D modelleri yükle
        self.modelleri_yukle()

        # UI'ı güncelle
        self.kontrol_paneli.adimlari_yukle(self.adim_yoneticisi.tum_adimlari_al())
        self.kontrol_paneli.parcalari_yukle(self.montaj_yoneticisi.tum_parcalari_al())

        # İlk adımı göster
        if self.adim_yoneticisi.adim_sayisi_al() > 0:
            self.adim_gorunumunu_guncelle()

        self.durum_cubugu.showMessage(
            f"Montaj yüklendi: {montaj_verisi['isim']} "
            f"({len(self.yuklenmis_modeller)} parça)"
        )

    def modelleri_yukle(self):
        """Montajdaki tüm 3D modelleri yükle"""
        proje_koku = proje_kok_dizini_al()
        model_dizini = proje_koku / self.konfig['paths']['models_dir']

        self.gorunum.sahneyi_temizle()
        self.yuklenmis_modeller.clear()

        for parca in self.montaj_yoneticisi.tum_parcalari_al():
            parca_id = parca['id']
            model_dosyasi = parca['model_dosyasi']
            renk = tuple(parca.get('renk', [0.8, 0.8, 0.8]))

            try:
                # Model dosyasını yükle
                model_yolu = model_dizini / model_dosyasi
                mesh = self.model_yukleyici.model_yukle(model_yolu)
                self.yuklenmis_modeller[parca_id] = mesh

                # Viewer'a ekle
                self.gorunum.mesh_ekle(parca_id, mesh, renk=renk)

                # Görünürlük ayarla
                gorunur = parca.get('gorunur', True)
                self.gorunum.mesh_gorunurlugunu_ayarla(parca_id, gorunur)

            except Exception as e:
                print(f"Model yüklenemedi [{parca_id}]: {str(e)}")

        self.gorunum.kamerayi_sifirla()

    def adim_gorunumunu_guncelle(self):
        """Mevcut adıma göre görünümü güncelle"""
        mevcut_adim = self.adim_yoneticisi.mevcut_adimi_al()
        mevcut_indeks = self.adim_yoneticisi.mevcut_adim_indeksi
        toplam_adim = self.adim_yoneticisi.adim_sayisi_al()

        # Kontrol panelini güncelle
        self.kontrol_paneli.adim_bilgisini_guncelle(mevcut_adim, mevcut_indeks, toplam_adim)

        if not mevcut_adim:
            return

        # Parça görünürlüklerini güncelle
        gorunur_parcalar = mevcut_adim.get('gorunur_parcalar', [])
        for parca_id in self.yuklenmis_modeller.keys():
            self.gorunum.mesh_gorunurlugunu_ayarla(parca_id, parca_id in gorunur_parcalar)

        # Vurgulanan parçalar
        vurgulu_parcalar = mevcut_adim.get('vurgulu_parcalar', [])
        for parca_id in self.yuklenmis_modeller.keys():
            if parca_id in vurgulu_parcalar:
                self.gorunum.mesh_vurgula(parca_id, True)
            else:
                # Orijinal renge dön
                parca = self.montaj_yoneticisi.parca_al(parca_id)
                if parca:
                    renk = tuple(parca.get('renk', [0.8, 0.8, 0.8]))
                    self.gorunum.mesh_rengini_ayarla(parca_id, renk)

        # Kamera pozisyonu
        kamera_poz = mevcut_adim.get('kamera_pozisyonu')
        if kamera_poz:
            self.gorunum.kamera_pozisyonunu_ayarla(kamera_poz, [0, 0, 0])

    def adim_degisti_slot(self, deger):
        """Adım değiştirildiğinde"""
        if deger == -1:
            # Önceki
            self.adim_yoneticisi.onceki_adim()
        elif deger == 1:
            # Sonraki
            self.adim_yoneticisi.sonraki_adim()
        elif deger == 0:
            # İlk
            self.adim_yoneticisi.adima_git(1)
        elif deger == 9999:
            # Son
            self.adim_yoneticisi.adima_git(self.adim_yoneticisi.adim_sayisi_al())
        elif deger >= 100:
            # Direkt adım (liste seçimi)
            self.adim_yoneticisi.adima_git(deger - 99)

        self.adim_gorunumunu_guncelle()

    def parca_secildi_slot(self, parca_id):
        """Parça seçildiğinde"""
        # Parçayı vurgula
        for pid in self.yuklenmis_modeller.keys():
            if pid == parca_id:
                self.gorunum.mesh_vurgula(pid, True)
            else:
                parca = self.montaj_yoneticisi.parca_al(pid)
                if parca:
                    renk = tuple(parca.get('renk', [0.8, 0.8, 0.8]))
                    self.gorunum.mesh_rengini_ayarla(pid, renk)

    def tam_ekran_degistir(self, secildi):
        """Tam ekran modunu aç/kapat"""
        if secildi:
            self.showFullScreen()
        else:
            self.showNormal()

    def hakkinda_goster(self):
        """Hakkında diyaloğu"""
        QMessageBox.about(
            self,
            "Hakkında",
            f"{self.konfig['app']['name']}\n"
            f"Versiyon: {self.konfig['app']['version']}\n\n"
            "3D montaj kılavuzu uygulaması\n"
            "SolidWorks CAD dosyalarından oluşturulan montaj talimatları"
        )

    def closeEvent(self, event):
        """Pencere kapatıldığında"""
        yanit = QMessageBox.question(
            self,
            'Çıkış',
            'Uygulamadan çıkmak istediğinize emin misiniz?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if yanit == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
