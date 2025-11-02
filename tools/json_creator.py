#!/usr/bin/env python3
"""
JSON Creator GUI - Montaj kilavuzu JSON dosyasi olusturucu

SolidWorks'ten export edilen STEP dosyalarindan otomatik JSON olusturur.
"""
import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QListWidget, QLabel,
                             QLineEdit, QTextEdit, QFileDialog, QMessageBox,
                             QColorDialog, QSpinBox, QGroupBox, QSplitter,
                             QListWidgetItem, QCheckBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
import json


class JSONCreatorGUI(QMainWindow):
    """JSON Creator ana pencere"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("JSON Creator - Montaj Kilavuzu")
        self.setGeometry(100, 100, 1400, 800)

        # Veri yapilari
        self.parcalar = []  # [{id, isim, dosya, renk, gorunur}]
        self.adimlar = []   # [{baslik, aciklama, gorunur_parcalar, vurgulu_parcalar}]
        self.step_klasoru = None

        self.arayuzu_olustur()

    def arayuzu_olustur(self):
        """Ana arayuzu olustur"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # Ust toolbar
        toolbar_layout = QHBoxLayout()

        self.btn_step_yukle = QPushButton("STEP Klasoru Sec")
        self.btn_step_yukle.clicked.connect(self.step_klasoru_sec)
        toolbar_layout.addWidget(self.btn_step_yukle)

        self.lbl_klasor = QLabel("Klasor secilmedi")
        toolbar_layout.addWidget(self.lbl_klasor)

        toolbar_layout.addStretch()

        self.btn_json_kaydet = QPushButton("JSON Kaydet")
        self.btn_json_kaydet.clicked.connect(self.json_kaydet)
        self.btn_json_kaydet.setEnabled(False)
        toolbar_layout.addWidget(self.btn_json_kaydet)

        main_layout.addLayout(toolbar_layout)

        # Ana icerik - 3 panel
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Sol panel: Parca listesi
        sol_panel = self.sol_panel_olustur()
        splitter.addWidget(sol_panel)

        # Orta panel: Parca duzenle
        orta_panel = self.orta_panel_olustur()
        splitter.addWidget(orta_panel)

        # Sag panel: Montaj adimlari
        sag_panel = self.sag_panel_olustur()
        splitter.addWidget(sag_panel)

        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 2)
        splitter.setStretchFactor(2, 3)

        main_layout.addWidget(splitter)

    def sol_panel_olustur(self):
        """Sol panel - Parca listesi"""
        panel = QGroupBox("Parca Listesi")
        layout = QVBoxLayout()

        # Bilgi
        info = QLabel("Export edilen STEP dosyalari:")
        layout.addWidget(info)

        # Liste
        self.parca_listesi = QListWidget()
        self.parca_listesi.currentRowChanged.connect(self.parca_secildi)
        layout.addWidget(self.parca_listesi)

        # Butonlar
        btn_layout = QHBoxLayout()

        self.btn_parca_sil = QPushButton("Parçayi Sil")
        self.btn_parca_sil.clicked.connect(self.parca_sil)
        self.btn_parca_sil.setEnabled(False)
        btn_layout.addWidget(self.btn_parca_sil)

        btn_layout.addStretch()

        layout.addLayout(btn_layout)

        # Toplam parca sayisi
        self.lbl_toplam = QLabel("Toplam: 0 parca")
        layout.addWidget(self.lbl_toplam)

        panel.setLayout(layout)
        return panel

    def orta_panel_olustur(self):
        """Orta panel - Parca duzenle"""
        panel = QGroupBox("Parca Ozellikleri")
        layout = QVBoxLayout()

        # ID
        lbl_id = QLabel("Parca ID:")
        self.txt_parca_id = QLineEdit()
        self.txt_parca_id.setReadOnly(True)
        layout.addWidget(lbl_id)
        layout.addWidget(self.txt_parca_id)

        # Isim
        lbl_isim = QLabel("Parca Ismi:")
        self.txt_parca_isim = QLineEdit()
        self.txt_parca_isim.textChanged.connect(self.parca_guncelle)
        layout.addWidget(lbl_isim)
        layout.addWidget(self.txt_parca_isim)

        # Dosya
        lbl_dosya = QLabel("STEP Dosyasi:")
        self.txt_parca_dosya = QLineEdit()
        self.txt_parca_dosya.setReadOnly(True)
        layout.addWidget(lbl_dosya)
        layout.addWidget(self.txt_parca_dosya)

        # Renk
        renk_layout = QHBoxLayout()
        lbl_renk = QLabel("Renk:")
        self.btn_renk_sec = QPushButton("Renk Sec")
        self.btn_renk_sec.clicked.connect(self.renk_sec)
        self.renk_ornek = QLabel("     ")
        self.renk_ornek.setStyleSheet("background-color: gray; border: 1px solid black;")
        renk_layout.addWidget(lbl_renk)
        renk_layout.addWidget(self.btn_renk_sec)
        renk_layout.addWidget(self.renk_ornek)
        renk_layout.addStretch()
        layout.addLayout(renk_layout)

        # Gorunurluk
        self.chk_gorunur = QCheckBox("Baslangicta gorunur")
        self.chk_gorunur.setChecked(True)
        self.chk_gorunur.stateChanged.connect(self.parca_guncelle)
        layout.addWidget(self.chk_gorunur)

        layout.addStretch()

        panel.setLayout(layout)
        panel.setEnabled(False)
        self.orta_panel = panel
        return panel

    def sag_panel_olustur(self):
        """Sag panel - Montaj adimlari"""
        panel = QGroupBox("Montaj Adimlari")
        layout = QVBoxLayout()

        # Adim listesi
        self.adim_listesi = QListWidget()
        self.adim_listesi.currentRowChanged.connect(self.adim_secildi)
        layout.addWidget(self.adim_listesi)

        # Butonlar
        btn_layout = QHBoxLayout()

        self.btn_adim_ekle = QPushButton("Adim Ekle")
        self.btn_adim_ekle.clicked.connect(self.adim_ekle)
        self.btn_adim_ekle.setEnabled(False)
        btn_layout.addWidget(self.btn_adim_ekle)

        self.btn_adim_sil = QPushButton("Adim Sil")
        self.btn_adim_sil.clicked.connect(self.adim_sil)
        self.btn_adim_sil.setEnabled(False)
        btn_layout.addWidget(self.btn_adim_sil)

        layout.addLayout(btn_layout)

        # Adim duzenleme
        self.adim_duzenleme = QWidget()
        adim_layout = QVBoxLayout()

        # Baslik
        lbl_baslik = QLabel("Adim Basligi:")
        self.txt_adim_baslik = QLineEdit()
        self.txt_adim_baslik.textChanged.connect(self.adim_guncelle)
        adim_layout.addWidget(lbl_baslik)
        adim_layout.addWidget(self.txt_adim_baslik)

        # Aciklama
        lbl_aciklama = QLabel("Aciklama:")
        self.txt_adim_aciklama = QTextEdit()
        self.txt_adim_aciklama.setMaximumHeight(100)
        self.txt_adim_aciklama.textChanged.connect(self.adim_guncelle)
        adim_layout.addWidget(lbl_aciklama)
        adim_layout.addWidget(self.txt_adim_aciklama)

        # Sure
        sure_layout = QHBoxLayout()
        lbl_sure = QLabel("Tahmini Sure (saniye):")
        self.spin_sure = QSpinBox()
        self.spin_sure.setRange(10, 600)
        self.spin_sure.setValue(60)
        self.spin_sure.valueChanged.connect(self.adim_guncelle)
        sure_layout.addWidget(lbl_sure)
        sure_layout.addWidget(self.spin_sure)
        sure_layout.addStretch()
        adim_layout.addLayout(sure_layout)

        # Gorunur parcalar (checkbox listesi olacak ama simdilik basit)
        lbl_gorunur = QLabel("Gorunur Parcalar (ID'ler, virgul ile ayirin):")
        self.txt_gorunur_parcalar = QLineEdit()
        self.txt_gorunur_parcalar.setPlaceholderText("parca_001, parca_002, parca_003")
        self.txt_gorunur_parcalar.textChanged.connect(self.adim_guncelle)
        adim_layout.addWidget(lbl_gorunur)
        adim_layout.addWidget(self.txt_gorunur_parcalar)

        # Vurgulu parcalar
        lbl_vurgulu = QLabel("Vurgulu Parcalar (ID'ler, virgul ile ayirin):")
        self.txt_vurgulu_parcalar = QLineEdit()
        self.txt_vurgulu_parcalar.setPlaceholderText("parca_001")
        self.txt_vurgulu_parcalar.textChanged.connect(self.adim_guncelle)
        adim_layout.addWidget(lbl_vurgulu)
        adim_layout.addWidget(self.txt_vurgulu_parcalar)

        self.adim_duzenleme.setLayout(adim_layout)
        self.adim_duzenleme.setEnabled(False)
        layout.addWidget(self.adim_duzenleme)

        panel.setLayout(layout)
        return panel

    def step_klasoru_sec(self):
        """STEP klasorunu sec ve dosyalari yukle"""
        klasor = QFileDialog.getExistingDirectory(self, "STEP Klasoru Sec")
        if not klasor:
            return

        self.step_klasoru = Path(klasor)
        self.lbl_klasor.setText(f"Klasor: {klasor}")

        # STEP dosyalarini tara
        step_dosyalari = list(self.step_klasoru.glob("*.step")) + \
                        list(self.step_klasoru.glob("*.stp")) + \
                        list(self.step_klasoru.glob("*.STEP")) + \
                        list(self.step_klasoru.glob("*.STP"))

        if not step_dosyalari:
            QMessageBox.warning(self, "Uyari", "Klasorde STEP dosyasi bulunamadi!")
            return

        # Parcalari olustur
        self.parcalar.clear()
        self.parca_listesi.clear()

        for i, dosya in enumerate(sorted(step_dosyalari), 1):
            parca = {
                'id': f"parca_{i:03d}",
                'isim': dosya.stem,  # Dosya adi (uzantisiz)
                'model_dosyasi': dosya.name,
                'renk': [0.7, 0.7, 0.7],  # Varsayilan gri
                'gorunur': True
            }
            self.parcalar.append(parca)
            self.parca_listesi.addItem(f"{parca['id']} - {parca['isim']}")

        self.lbl_toplam.setText(f"Toplam: {len(self.parcalar)} parca")
        self.btn_json_kaydet.setEnabled(True)
        self.btn_adim_ekle.setEnabled(True)

        QMessageBox.information(self, "Basarili",
                               f"{len(self.parcalar)} adet STEP dosyasi yuklendi!")

    def parca_secildi(self, index):
        """Parca listesinden parca secildiginde"""
        if index < 0 or index >= len(self.parcalar):
            self.orta_panel.setEnabled(False)
            return

        parca = self.parcalar[index]

        self.txt_parca_id.setText(parca['id'])
        self.txt_parca_isim.setText(parca['isim'])
        self.txt_parca_dosya.setText(parca['model_dosyasi'])
        self.chk_gorunur.setChecked(parca['gorunur'])

        # Renk goster
        renk = parca['renk']
        r, g, b = int(renk[0]*255), int(renk[1]*255), int(renk[2]*255)
        self.renk_ornek.setStyleSheet(
            f"background-color: rgb({r},{g},{b}); border: 1px solid black;"
        )

        self.orta_panel.setEnabled(True)
        self.btn_parca_sil.setEnabled(True)

    def renk_sec(self):
        """Renk sec dialogu"""
        index = self.parca_listesi.currentRow()
        if index < 0:
            return

        parca = self.parcalar[index]

        # Mevcut rengi QColor'a cevir
        r, g, b = parca['renk']
        mevcut_renk = QColor(int(r*255), int(g*255), int(b*255))

        renk = QColorDialog.getColor(mevcut_renk, self, "Parca Rengi Sec")
        if renk.isValid():
            # RGB'yi 0-1 araligina cevir
            parca['renk'] = [renk.red()/255, renk.green()/255, renk.blue()/255]

            # Ornegi guncelle
            self.renk_ornek.setStyleSheet(
                f"background-color: {renk.name()}; border: 1px solid black;"
            )

    def parca_guncelle(self):
        """Secili parcanin ozelliklerini guncelle"""
        index = self.parca_listesi.currentRow()
        if index < 0:
            return

        parca = self.parcalar[index]
        parca['isim'] = self.txt_parca_isim.text()
        parca['gorunur'] = self.chk_gorunur.isChecked()

        # Listeyi guncelle
        self.parca_listesi.item(index).setText(f"{parca['id']} - {parca['isim']}")

    def parca_sil(self):
        """Secili parcayi sil"""
        index = self.parca_listesi.currentRow()
        if index < 0:
            return

        yanit = QMessageBox.question(self, "Emin misiniz?",
                                     "Bu parcayi silmek istediginizden emin misiniz?")
        if yanit == QMessageBox.StandardButton.Yes:
            del self.parcalar[index]
            self.parca_listesi.takeItem(index)
            self.lbl_toplam.setText(f"Toplam: {len(self.parcalar)} parca")

    def adim_ekle(self):
        """Yeni montaj adimi ekle"""
        adim_no = len(self.adimlar) + 1
        adim = {
            'adim_numarasi': adim_no,
            'baslik': f"Adim {adim_no}",
            'aciklama': "",
            'gorunur_parcalar': [],
            'vurgulu_parcalar': [],
            'kamera_pozisyonu': [100, 100, 100],
            'sure': 60
        }
        self.adimlar.append(adim)
        self.adim_listesi.addItem(f"{adim_no}. {adim['baslik']}")
        self.adim_listesi.setCurrentRow(len(self.adimlar) - 1)

    def adim_secildi(self, index):
        """Adim listesinden adim secildiginde"""
        if index < 0 or index >= len(self.adimlar):
            self.adim_duzenleme.setEnabled(False)
            return

        adim = self.adimlar[index]

        self.txt_adim_baslik.setText(adim['baslik'])
        self.txt_adim_aciklama.setPlainText(adim['aciklama'])
        self.spin_sure.setValue(adim['sure'])

        # Parcalari string'e cevir
        gorunur_str = ", ".join(adim['gorunur_parcalar'])
        vurgulu_str = ", ".join(adim['vurgulu_parcalar'])

        self.txt_gorunur_parcalar.setText(gorunur_str)
        self.txt_vurgulu_parcalar.setText(vurgulu_str)

        self.adim_duzenleme.setEnabled(True)
        self.btn_adim_sil.setEnabled(True)

    def adim_guncelle(self):
        """Secili adimi guncelle"""
        index = self.adim_listesi.currentRow()
        if index < 0:
            return

        adim = self.adimlar[index]
        adim['baslik'] = self.txt_adim_baslik.text()
        adim['aciklama'] = self.txt_adim_aciklama.toPlainText()
        adim['sure'] = self.spin_sure.value()

        # String'den listeye cevir
        gorunur_str = self.txt_gorunur_parcalar.text()
        vurgulu_str = self.txt_vurgulu_parcalar.text()

        adim['gorunur_parcalar'] = [p.strip() for p in gorunur_str.split(',') if p.strip()]
        adim['vurgulu_parcalar'] = [p.strip() for p in vurgulu_str.split(',') if p.strip()]

        # Listeyi guncelle
        self.adim_listesi.item(index).setText(f"{adim['adim_numarasi']}. {adim['baslik']}")

    def adim_sil(self):
        """Secili adimi sil"""
        index = self.adim_listesi.currentRow()
        if index < 0:
            return

        yanit = QMessageBox.question(self, "Emin misiniz?",
                                     "Bu adimi silmek istediginizden emin misiniz?")
        if yanit == QMessageBox.StandardButton.Yes:
            del self.adimlar[index]
            self.adim_listesi.takeItem(index)

            # Adim numaralarini yeniden duzenle
            for i, adim in enumerate(self.adimlar, 1):
                adim['adim_numarasi'] = i
                self.adim_listesi.item(i-1).setText(f"{i}. {adim['baslik']}")

    def json_kaydet(self):
        """JSON dosyasini kaydet"""
        if not self.parcalar:
            QMessageBox.warning(self, "Uyari", "Parca listesi bos!")
            return

        # Kayit yeri sec
        dosya, _ = QFileDialog.getSaveFileName(
            self,
            "JSON Kaydet",
            "montaj.json",
            "JSON Files (*.json)"
        )

        if not dosya:
            return

        # JSON olustur
        montaj = {
            'isim': Path(dosya).stem,
            'aciklama': f"{len(self.parcalar)} parcali montaj",
            'parcalar': self.parcalar,
            'adimlar': self.adimlar
        }

        # Kaydet
        try:
            with open(dosya, 'w', encoding='utf-8') as f:
                json.dump(montaj, f, indent=2, ensure_ascii=False)

            QMessageBox.information(self, "Basarili",
                                   f"JSON dosyasi kaydedildi:\n{dosya}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"JSON kaydetme hatasi:\n{str(e)}")


def main():
    """Ana fonksiyon"""
    app = QApplication(sys.argv)
    app.setApplicationName("JSON Creator")

    pencere = JSONCreatorGUI()
    pencere.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
