"""
Montaj adimlarini kontrol eden panel
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QTextEdit, QListWidget, QProgressBar,
                             QGroupBox)
from PyQt6.QtCore import Qt, pyqtSignal


class KontrolPaneli(QWidget):
    """Montaj kontrol paneli"""

    # Signals
    adim_degisti = pyqtSignal(int)  # Adim degistiginde
    parca_secildi = pyqtSignal(str)  # Parca secildiginde

    def __init__(self, parent=None):
        super().__init__(parent)
        self.arayuzu_olustur()

    def arayuzu_olustur(self):
        """UI elemanlarini olustur"""
        layout = QVBoxLayout(self)

        # Baslik
        baslik = QLabel("Montaj Adimlari")
        baslik.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(baslik)

        # Ilerleme cubugu
        ilerleme_grubu = QGroupBox("Ilerleme")
        ilerleme_layout = QVBoxLayout()
        self.ilerleme_cubugu = QProgressBar()
        self.ilerleme_cubugu.setMinimum(0)
        self.ilerleme_cubugu.setMaximum(100)
        self.ilerleme_etiketi = QLabel("Adim 0 / 0")
        ilerleme_layout.addWidget(self.ilerleme_cubugu)
        ilerleme_layout.addWidget(self.ilerleme_etiketi)
        ilerleme_grubu.setLayout(ilerleme_layout)
        layout.addWidget(ilerleme_grubu)

        # Mevcut adim bilgisi
        adim_grubu = QGroupBox("Mevcut Adim")
        adim_layout = QVBoxLayout()

        self.adim_basligi = QLabel("Adim basligi")
        self.adim_basligi.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.adim_basligi.setWordWrap(True)

        self.adim_aciklamasi = QTextEdit()
        self.adim_aciklamasi.setReadOnly(True)
        self.adim_aciklamasi.setMaximumHeight(100)

        adim_layout.addWidget(self.adim_basligi)
        adim_layout.addWidget(self.adim_aciklamasi)
        adim_grubu.setLayout(adim_layout)
        layout.addWidget(adim_grubu)

        # Navigasyon butonlari
        nav_layout = QHBoxLayout()

        self.btn_ilk = QPushButton("⏮ Ilk")
        self.btn_onceki = QPushButton("◀ Onceki")
        self.btn_sonraki = QPushButton("Sonraki ▶")
        self.btn_son = QPushButton("Son ⏭")

        self.btn_ilk.clicked.connect(self.ilk_tiklandi)
        self.btn_onceki.clicked.connect(self.onceki_tiklandi)
        self.btn_sonraki.clicked.connect(self.sonraki_tiklandi)
        self.btn_son.clicked.connect(self.son_tiklandi)

        nav_layout.addWidget(self.btn_ilk)
        nav_layout.addWidget(self.btn_onceki)
        nav_layout.addWidget(self.btn_sonraki)
        nav_layout.addWidget(self.btn_son)

        layout.addLayout(nav_layout)

        # Adim listesi
        adimlar_grubu = QGroupBox("Tum Adimlar")
        adimlar_layout = QVBoxLayout()
        self.adimlar_listesi = QListWidget()
        self.adimlar_listesi.currentRowChanged.connect(self.adim_listesi_degisti)
        adimlar_layout.addWidget(self.adimlar_listesi)
        adimlar_grubu.setLayout(adimlar_layout)
        layout.addWidget(adimlar_grubu)

        # Parca listesi
        parcalar_grubu = QGroupBox("Parcalar")
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
        Adim bilgilerini guncelle

        Args:
            adim (dict): Adim bilgisi
            mevcut_indeks (int): Mevcut adim indexi (0-based)
            toplam_adim (int): Toplam adim sayisi
        """
        if adim:
            self.adim_basligi.setText(adim.get('baslik', 'Baslik yok'))
            self.adim_aciklamasi.setPlainText(adim.get('aciklama', 'Aciklama yok'))
        else:
            self.adim_basligi.setText("Adim yok")
            self.adim_aciklamasi.setPlainText("")

        # Ilerleme guncelle
        if toplam_adim > 0:
            ilerleme = int(((mevcut_indeks + 1) / toplam_adim) * 100)
            self.ilerleme_cubugu.setValue(ilerleme)
            self.ilerleme_etiketi.setText(f"Adim {mevcut_indeks + 1} / {toplam_adim}")
        else:
            self.ilerleme_cubugu.setValue(0)
            self.ilerleme_etiketi.setText("Adim 0 / 0")

        # Buton durumlari
        self.btn_ilk.setEnabled(mevcut_indeks > 0)
        self.btn_onceki.setEnabled(mevcut_indeks > 0)
        self.btn_sonraki.setEnabled(mevcut_indeks < toplam_adim - 1)
        self.btn_son.setEnabled(mevcut_indeks < toplam_adim - 1)

        # Listede sec
        if 0 <= mevcut_indeks < self.adimlar_listesi.count():
            self.adimlar_listesi.setCurrentRow(mevcut_indeks)

    def adimlari_yukle(self, adimlar):
        """Adim listesini yukle"""
        self.adimlar_listesi.clear()
        for i, adim in enumerate(adimlar):
            self.adimlar_listesi.addItem(f"{i+1}. {adim.get('baslik', 'Isimsiz')}")

    def parcalari_yukle(self, parcalar):
        """Parca listesini yukle"""
        self.parcalar_listesi.clear()
        for parca in parcalar:
            self.parcalar_listesi.addItem(f"{parca.get('isim', 'Isimsiz')} [{parca.get('id')}]")

    def ilk_tiklandi(self):
        """Ilk adima git"""
        self.adim_degisti.emit(0)

    def onceki_tiklandi(self):
        """Onceki adim"""
        self.adim_degisti.emit(-1)  # -1 = onceki

    def sonraki_tiklandi(self):
        """Sonraki adim"""
        self.adim_degisti.emit(1)  # 1 = sonraki

    def son_tiklandi(self):
        """Son adima git"""
        self.adim_degisti.emit(9999)  # Buyuk sayi = son

    def adim_listesi_degisti(self, indeks):
        """Liste uzerinden adim degistirildi"""
        if indeks >= 0:
            self.adim_degisti.emit(indeks + 100)  # +100 = direkt adim

    def parca_secildi_slot(self, metin):
        """Parca secildi"""
        if metin:
            # ID'yi ayikla [id] formatindan
            parca_id = metin.split('[')[-1].replace(']', '').strip()
            self.parca_secildi.emit(parca_id)
