"""
Montaj adımlarını kontrol eden panel
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QTextEdit, QListWidget, QProgressBar,
                             QGroupBox)
from PyQt6.QtCore import Qt, pyqtSignal


class KontrolPaneli(QWidget):
    """Montaj kontrol paneli"""

    # Signals
    adim_degisti = pyqtSignal(int)  # Adım değiştiğinde
    parca_secildi = pyqtSignal(str)  # Parça seçildiğinde

    def __init__(self, parent=None):
        super().__init__(parent)
        self.arayuzu_olustur()

    def arayuzu_olustur(self):
        """UI elemanlarını oluştur"""
        layout = QVBoxLayout(self)

        # Başlık
        baslik = QLabel("Montaj Adımları")
        baslik.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(baslik)

        # İlerleme çubuğu
        ilerleme_grubu = QGroupBox("İlerleme")
        ilerleme_layout = QVBoxLayout()
        self.ilerleme_cubugu = QProgressBar()
        self.ilerleme_cubugu.setMinimum(0)
        self.ilerleme_cubugu.setMaximum(100)
        self.ilerleme_etiketi = QLabel("Adım 0 / 0")
        ilerleme_layout.addWidget(self.ilerleme_cubugu)
        ilerleme_layout.addWidget(self.ilerleme_etiketi)
        ilerleme_grubu.setLayout(ilerleme_layout)
        layout.addWidget(ilerleme_grubu)

        # Mevcut adım bilgisi
        adim_grubu = QGroupBox("Mevcut Adım")
        adim_layout = QVBoxLayout()

        self.adim_basligi = QLabel("Adım başlığı")
        self.adim_basligi.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.adim_basligi.setWordWrap(True)

        self.adim_aciklamasi = QTextEdit()
        self.adim_aciklamasi.setReadOnly(True)
        self.adim_aciklamasi.setMaximumHeight(100)

        adim_layout.addWidget(self.adim_basligi)
        adim_layout.addWidget(self.adim_aciklamasi)
        adim_grubu.setLayout(adim_layout)
        layout.addWidget(adim_grubu)

        # Navigasyon butonları
        nav_layout = QHBoxLayout()

        self.btn_ilk = QPushButton("⏮ İlk")
        self.btn_onceki = QPushButton("◀ Önceki")
        self.btn_sonraki = QPushButton("Sonraki ▶")
        self.btn_son = QPushButton("Son ⏭")

        self.btn_ilk.clicked.connect(self.ilk_tiklandı)
        self.btn_onceki.clicked.connect(self.onceki_tiklandı)
        self.btn_sonraki.clicked.connect(self.sonraki_tiklandı)
        self.btn_son.clicked.connect(self.son_tiklandı)

        nav_layout.addWidget(self.btn_ilk)
        nav_layout.addWidget(self.btn_onceki)
        nav_layout.addWidget(self.btn_sonraki)
        nav_layout.addWidget(self.btn_son)

        layout.addLayout(nav_layout)

        # Adım listesi
        adimlar_grubu = QGroupBox("Tüm Adımlar")
        adimlar_layout = QVBoxLayout()
        self.adimlar_listesi = QListWidget()
        self.adimlar_listesi.currentRowChanged.connect(self.adim_listesi_degisti)
        adimlar_layout.addWidget(self.adimlar_listesi)
        adimlar_grubu.setLayout(adimlar_layout)
        layout.addWidget(adimlar_grubu)

        # Parça listesi
        parcalar_grubu = QGroupBox("Parçalar")
        parcalar_layout = QVBoxLayout()
        self.parcalar_listesi = QListWidget()
        self.parcalar_listesi.currentTextChanged.connect(self.parca_secildi_slot)
        parcalar_layout.addWidget(self.parcalar_listesi)
        parcalar_grubu.setLayout(parcalar_layout)
        layout.addWidget(parcalar_grubu)

        # Stretch
        layout.addStretch()

    def adim_bilgisini_guncelle(self, adim, mevcut_indeks, toplam_adim):
        """
        Adım bilgilerini güncelle

        Args:
            adim (dict): Adım bilgisi
            mevcut_indeks (int): Mevcut adım indexi (0-based)
            toplam_adim (int): Toplam adım sayısı
        """
        if adim:
            self.adim_basligi.setText(adim.get('baslik', 'Başlık yok'))
            self.adim_aciklamasi.setPlainText(adim.get('aciklama', 'Açıklama yok'))
        else:
            self.adim_basligi.setText("Adım yok")
            self.adim_aciklamasi.setPlainText("")

        # İlerleme güncelle
        if toplam_adim > 0:
            ilerleme = int(((mevcut_indeks + 1) / toplam_adim) * 100)
            self.ilerleme_cubugu.setValue(ilerleme)
            self.ilerleme_etiketi.setText(f"Adım {mevcut_indeks + 1} / {toplam_adim}")
        else:
            self.ilerleme_cubugu.setValue(0)
            self.ilerleme_etiketi.setText("Adım 0 / 0")

        # Buton durumları
        self.btn_ilk.setEnabled(mevcut_indeks > 0)
        self.btn_onceki.setEnabled(mevcut_indeks > 0)
        self.btn_sonraki.setEnabled(mevcut_indeks < toplam_adim - 1)
        self.btn_son.setEnabled(mevcut_indeks < toplam_adim - 1)

        # Listede seç
        if 0 <= mevcut_indeks < self.adimlar_listesi.count():
            self.adimlar_listesi.setCurrentRow(mevcut_indeks)

    def adimlari_yukle(self, adimlar):
        """Adım listesini yükle"""
        self.adimlar_listesi.clear()
        for i, adim in enumerate(adimlar):
            self.adimlar_listesi.addItem(f"{i+1}. {adim.get('baslik', 'İsimsiz')}")

    def parcalari_yukle(self, parcalar):
        """Parça listesini yükle"""
        self.parcalar_listesi.clear()
        for parca in parcalar:
            self.parcalar_listesi.addItem(f"{parca.get('isim', 'İsimsiz')} [{parca.get('id')}]")

    def ilk_tiklandı(self):
        """İlk adıma git"""
        self.adim_degisti.emit(0)

    def onceki_tiklandı(self):
        """Önceki adım"""
        self.adim_degisti.emit(-1)  # -1 = önceki

    def sonraki_tiklandı(self):
        """Sonraki adım"""
        self.adim_degisti.emit(1)  # 1 = sonraki

    def son_tiklandı(self):
        """Son adıma git"""
        self.adim_degisti.emit(9999)  # Büyük sayı = son

    def adim_listesi_degisti(self, indeks):
        """Liste üzerinden adım değiştirildi"""
        if indeks >= 0:
            self.adim_degisti.emit(indeks + 100)  # +100 = direkt adım

    def parca_secildi_slot(self, metin):
        """Parça seçildi"""
        if metin:
            # ID'yi ayıkla [id] formatından
            parca_id = metin.split('[')[-1].replace(']', '').strip()
            self.parca_secildi.emit(parca_id)
