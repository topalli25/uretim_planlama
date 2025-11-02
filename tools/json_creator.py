#!/usr/bin/env python3
"""
JSON Creator GUI - Montaj kilavuzu JSON dosyasi olusturucu (3D Onizlemeli)

SolidWorks'ten export edilen STEP dosyalarindan otomatik JSON olusturur.
3D onizleme ile parcalari gercek zamanli goruntule!
"""
import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QListWidget, QLabel,
                             QLineEdit, QTextEdit, QFileDialog, QMessageBox,
                             QColorDialog, QSpinBox, QGroupBox, QSplitter,
                             QListWidgetItem, QCheckBox, QTabWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
import json

# 3D gorselestirme icin
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.gui.gorunum_widget import GorunumWidget
from src.core.model_yukleyici import ModelYukleyici


class JSONCreatorGUI(QMainWindow):
    """JSON Creator ana pencere (3D Onizlemeli)"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("JSON Creator - 3D Montaj Kilavuzu Olusturucu")
        self.setGeometry(50, 50, 1600, 900)

        # Veri yapilari
        self.parcalar = []  # [{id, isim, dosya, renk, gorunur}]
        self.adimlar = []   # [{baslik, aciklama, gorunur_parcalar, vurgulu_parcalar}]
        self.step_klasoru = None
        self.yuklenmis_meshler = {}  # {parca_id: mesh}

        # Model yukleyici
        self.model_yukleyici = ModelYukleyici()

        self.arayuzu_olustur()

    def arayuzu_olustur(self):
        """Ana arayuzu olustur"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # Ust toolbar
        toolbar_layout = QHBoxLayout()

        self.btn_step_yukle = QPushButton("📂 STEP Klasoru Sec")
        self.btn_step_yukle.clicked.connect(self.step_klasoru_sec)
        toolbar_layout.addWidget(self.btn_step_yukle)

        self.lbl_klasor = QLabel("Klasor secilmedi")
        toolbar_layout.addWidget(self.lbl_klasor)

        toolbar_layout.addStretch()

        self.btn_kamera_kaydet = QPushButton("📷 Kamera Pozisyonu Kaydet")
        self.btn_kamera_kaydet.clicked.connect(self.kamera_pozisyonu_kaydet)
        self.btn_kamera_kaydet.setEnabled(False)
        toolbar_layout.addWidget(self.btn_kamera_kaydet)

        self.btn_json_kaydet = QPushButton("💾 JSON Kaydet")
        self.btn_json_kaydet.clicked.connect(self.json_kaydet)
        self.btn_json_kaydet.setEnabled(False)
        toolbar_layout.addWidget(self.btn_json_kaydet)

        main_layout.addLayout(toolbar_layout)

        # Ana icerik - 3 panel
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Sol panel: Parca listesi
        sol_panel = self.sol_panel_olustur()
        splitter.addWidget(sol_panel)

        # Orta panel: 3D gorunum + Parca duzenle
        orta_panel = self.orta_panel_olustur()
        splitter.addWidget(orta_panel)

        # Sag panel: Montaj adimlari
        sag_panel = self.sag_panel_olustur()
        splitter.addWidget(sag_panel)

        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 4)
        splitter.setStretchFactor(2, 3)

        main_layout.addWidget(splitter)

        # Status bar
        self.statusBar().showMessage("Hazir - STEP klasoru secin")

    def sol_panel_olustur(self):
        """Sol panel - Parca listesi"""
        panel = QGroupBox("📦 Parca Listesi")
        layout = QVBoxLayout()

        # Arama
        arama_layout = QHBoxLayout()
        lbl_ara = QLabel("Ara:")
        self.txt_ara = QLineEdit()
        self.txt_ara.setPlaceholderText("Parca adi veya ID...")
        self.txt_ara.textChanged.connect(self.parcalari_filtrele)
        arama_layout.addWidget(lbl_ara)
        arama_layout.addWidget(self.txt_ara)
        layout.addLayout(arama_layout)

        # Liste
        self.parca_listesi = QListWidget()
        self.parca_listesi.currentRowChanged.connect(self.parca_secildi)
        layout.addWidget(self.parca_listesi)

        # Butonlar
        btn_layout = QHBoxLayout()

        self.btn_parca_sil = QPushButton("🗑 Sil")
        self.btn_parca_sil.clicked.connect(self.parca_sil)
        self.btn_parca_sil.setEnabled(False)
        btn_layout.addWidget(self.btn_parca_sil)

        self.btn_tum_parcalari_goster = QPushButton("👁 Hepsini Goster")
        self.btn_tum_parcalari_goster.clicked.connect(self.tum_parcalari_goster)
        self.btn_tum_parcalari_goster.setEnabled(False)
        btn_layout.addWidget(self.btn_tum_parcalari_goster)

        layout.addLayout(btn_layout)

        # Toplam parca sayisi
        self.lbl_toplam = QLabel("Toplam: 0 parca")
        layout.addWidget(self.lbl_toplam)

        panel.setLayout(layout)
        return panel

    def orta_panel_olustur(self):
        """Orta panel - 3D Gorunum + Parca Duzenle"""
        panel = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Tab widget (3D / Duzenle)
        tabs = QTabWidget()

        # Tab 1: 3D Gorunum
        tab_3d = QWidget()
        tab_3d_layout = QVBoxLayout()
        tab_3d_layout.setContentsMargins(0, 0, 0, 0)

        # 3D Widget
        self.gorunum_3d = GorunumWidget()
        tab_3d_layout.addWidget(self.gorunum_3d)

        # Kontroller
        kontrol_layout = QHBoxLayout()

        btn_sifirla = QPushButton("🔄 Kamera Sifirla")
        btn_sifirla.clicked.connect(self.gorunum_3d.kamerayi_sifirla)
        kontrol_layout.addWidget(btn_sifirla)

        btn_temizle = QPushButton("🧹 Temizle")
        btn_temizle.clicked.connect(self.gorunum_3d.sahneyi_temizle)
        kontrol_layout.addWidget(btn_temizle)

        kontrol_layout.addStretch()

        self.lbl_3d_bilgi = QLabel("Model yuklu degil")
        kontrol_layout.addWidget(self.lbl_3d_bilgi)

        tab_3d_layout.addLayout(kontrol_layout)
        tab_3d.setLayout(tab_3d_layout)

        # Tab 2: Parca Duzenle
        tab_duzenle = QWidget()
        tab_duzenle_layout = QVBoxLayout()

        # ID
        lbl_id = QLabel("Parca ID:")
        self.txt_parca_id = QLineEdit()
        self.txt_parca_id.setReadOnly(True)
        tab_duzenle_layout.addWidget(lbl_id)
        tab_duzenle_layout.addWidget(self.txt_parca_id)

        # Isim
        lbl_isim = QLabel("Parca Ismi:")
        self.txt_parca_isim = QLineEdit()
        self.txt_parca_isim.textChanged.connect(self.parca_guncelle)
        tab_duzenle_layout.addWidget(lbl_isim)
        tab_duzenle_layout.addWidget(self.txt_parca_isim)

        # Dosya
        lbl_dosya = QLabel("STEP Dosyasi:")
        self.txt_parca_dosya = QLineEdit()
        self.txt_parca_dosya.setReadOnly(True)
        tab_duzenle_layout.addWidget(lbl_dosya)
        tab_duzenle_layout.addWidget(self.txt_parca_dosya)

        # Renk
        renk_layout = QHBoxLayout()
        lbl_renk = QLabel("Renk:")
        self.btn_renk_sec = QPushButton("🎨 Renk Sec")
        self.btn_renk_sec.clicked.connect(self.renk_sec)
        self.renk_ornek = QLabel("     ")
        self.renk_ornek.setStyleSheet("background-color: gray; border: 1px solid black;")
        renk_layout.addWidget(lbl_renk)
        renk_layout.addWidget(self.btn_renk_sec)
        renk_layout.addWidget(self.renk_ornek)
        renk_layout.addStretch()
        tab_duzenle_layout.addLayout(renk_layout)

        # Gorunurluk
        self.chk_gorunur = QCheckBox("Baslangicta gorunur")
        self.chk_gorunur.setChecked(True)
        self.chk_gorunur.stateChanged.connect(self.parca_guncelle)
        tab_duzenle_layout.addWidget(self.chk_gorunur)

        # Model bilgisi
        self.lbl_model_bilgi = QLabel("")
        self.lbl_model_bilgi.setStyleSheet("color: gray; font-size: 10px;")
        tab_duzenle_layout.addWidget(self.lbl_model_bilgi)

        tab_duzenle_layout.addStretch()

        tab_duzenle.setLayout(tab_duzenle_layout)

        # Tablari ekle
        tabs.addTab(tab_3d, "🎬 3D Onizleme")
        tabs.addTab(tab_duzenle, "✏️ Parca Duzenle")

        layout.addWidget(tabs)
        panel.setLayout(layout)

        self.orta_tabs = tabs
        return panel

    def sag_panel_olustur(self):
        """Sag panel - Montaj adimlari"""
        panel = QGroupBox("📋 Montaj Adimlari")
        layout = QVBoxLayout()

        # Adim listesi
        self.adim_listesi = QListWidget()
        self.adim_listesi.currentRowChanged.connect(self.adim_secildi)
        layout.addWidget(self.adim_listesi)

        # Butonlar
        btn_layout = QHBoxLayout()

        self.btn_adim_ekle = QPushButton("➕ Adim Ekle")
        self.btn_adim_ekle.clicked.connect(self.adim_ekle)
        self.btn_adim_ekle.setEnabled(False)
        btn_layout.addWidget(self.btn_adim_ekle)

        self.btn_adim_sil = QPushButton("🗑 Sil")
        self.btn_adim_sil.clicked.connect(self.adim_sil)
        self.btn_adim_sil.setEnabled(False)
        btn_layout.addWidget(self.btn_adim_sil)

        self.btn_adim_onizle = QPushButton("👁 Onizle")
        self.btn_adim_onizle.clicked.connect(self.adim_onizle)
        self.btn_adim_onizle.setEnabled(False)
        btn_layout.addWidget(self.btn_adim_onizle)

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
        self.txt_adim_aciklama.setMaximumHeight(80)
        self.txt_adim_aciklama.textChanged.connect(self.adim_guncelle)
        adim_layout.addWidget(lbl_aciklama)
        adim_layout.addWidget(self.txt_adim_aciklama)

        # Sure
        sure_layout = QHBoxLayout()
        lbl_sure = QLabel("Sure (sn):")
        self.spin_sure = QSpinBox()
        self.spin_sure.setRange(10, 600)
        self.spin_sure.setValue(60)
        self.spin_sure.valueChanged.connect(self.adim_guncelle)
        sure_layout.addWidget(lbl_sure)
        sure_layout.addWidget(self.spin_sure)
        sure_layout.addStretch()
        adim_layout.addLayout(sure_layout)

        # Gorunur parcalar
        lbl_gorunur = QLabel("Gorunur Parcalar (virgul ile ayir):")
        self.txt_gorunur_parcalar = QLineEdit()
        self.txt_gorunur_parcalar.setPlaceholderText("parca_001, parca_002, parca_003")
        self.txt_gorunur_parcalar.textChanged.connect(self.adim_guncelle)
        adim_layout.addWidget(lbl_gorunur)
        adim_layout.addWidget(self.txt_gorunur_parcalar)

        # Vurgulu parcalar
        lbl_vurgulu = QLabel("Vurgulu Parcalar (virgul ile ayir):")
        self.txt_vurgulu_parcalar = QLineEdit()
        self.txt_vurgulu_parcalar.setPlaceholderText("parca_001")
        self.txt_vurgulu_parcalar.textChanged.connect(self.adim_guncelle)
        adim_layout.addWidget(lbl_vurgulu)
        adim_layout.addWidget(self.txt_vurgulu_parcalar)

        # Kamera pozisyonu
        lbl_kamera = QLabel("Kamera Pozisyonu [x, y, z]:")
        self.txt_kamera_poz = QLineEdit()
        self.txt_kamera_poz.setText("[100, 100, 100]")
        self.txt_kamera_poz.textChanged.connect(self.adim_guncelle)
        adim_layout.addWidget(lbl_kamera)
        adim_layout.addWidget(self.txt_kamera_poz)

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
        self.lbl_klasor.setText(f"📂 {klasor}")

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
        self.gorunum_3d.sahneyi_temizle()
        self.yuklenmis_meshler.clear()

        self.statusBar().showMessage("STEP dosyalari yukleniyor...")

        for i, dosya in enumerate(sorted(step_dosyalari), 1):
            parca = {
                'id': f"parca_{i:03d}",
                'isim': dosya.stem,
                'model_dosyasi': dosya.name,
                'renk': [0.7, 0.7, 0.7],
                'gorunur': True
            }
            self.parcalar.append(parca)
            self.parca_listesi.addItem(f"{parca['id']} - {parca['isim']}")

        self.lbl_toplam.setText(f"Toplam: {len(self.parcalar)} parca")
        self.btn_json_kaydet.setEnabled(True)
        self.btn_adim_ekle.setEnabled(True)
        self.btn_tum_parcalari_goster.setEnabled(True)
        self.btn_kamera_kaydet.setEnabled(True)

        self.statusBar().showMessage(f"{len(self.parcalar)} parca yuklendi!")

        QMessageBox.information(self, "Basarili",
                               f"{len(self.parcalar)} adet STEP dosyasi yuklendi!\n\n"
                               "Parcalari goruntulemek icin:\n"
                               "1. Sol panelden parca secin\n"
                               "2. Veya 'Hepsini Goster' butonuna tiklayin")

    def parca_secildi(self, index):
        """Parca listesinden parca secildiginde - 3D'de goster"""
        if index < 0 or index >= len(self.parcalar):
            self.orta_tabs.setTabEnabled(1, False)
            return

        parca = self.parcalar[index]

        # Form alanlari doldur
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

        self.orta_tabs.setTabEnabled(1, True)
        self.btn_parca_sil.setEnabled(True)

        # 3D'de goster
        self.parcayi_3d_goster(parca)

    def parcayi_3d_goster(self, parca):
        """Parcayi 3D gorunumde goster"""
        parca_id = parca['id']

        # Eger mesh yuklenmemisse yukle
        if parca_id not in self.yuklenmis_meshler:
            try:
                dosya_yolu = self.step_klasoru / parca['model_dosyasi']
                mesh = self.model_yukleyici.model_yukle(dosya_yolu)
                self.yuklenmis_meshler[parca_id] = mesh

                # Model bilgisi
                bilgi = self.model_yukleyici.model_bilgisi_al(mesh)
                self.lbl_model_bilgi.setText(
                    f"Nokta: {bilgi['nokta_sayisi']:,} | "
                    f"Yuzey: {bilgi['yuzey_sayisi']:,} | "
                    f"Hacim: {bilgi['hacim']:.2f}"
                )
            except Exception as e:
                QMessageBox.warning(self, "Hata", f"Model yuklenemedi:\n{str(e)}")
                return

        # Sahneyi temizle ve bu parcayi goster
        self.gorunum_3d.sahneyi_temizle()

        mesh = self.yuklenmis_meshler[parca_id]
        renk = tuple(parca['renk'])

        self.gorunum_3d.mesh_ekle(parca_id, mesh, renk=renk)
        self.gorunum_3d.kamerayi_sifirla()

        self.lbl_3d_bilgi.setText(f"Goruntulen: {parca['isim']}")
        self.statusBar().showMessage(f"3D: {parca['isim']} yuklendi")

    def tum_parcalari_goster(self):
        """Tum parcalari 3D'de goster"""
        self.gorunum_3d.sahneyi_temizle()

        yuklenen = 0
        toplam = len(self.parcalar)

        self.statusBar().showMessage(f"Tum parcalar yukleniyor... 0/{toplam}")

        for i, parca in enumerate(self.parcalar, 1):
            try:
                parca_id = parca['id']

                # Mesh yukle (cache'den veya diskten)
                if parca_id not in self.yuklenmis_meshler:
                    dosya_yolu = self.step_klasoru / parca['model_dosyasi']
                    mesh = self.model_yukleyici.model_yukle(dosya_yolu)
                    self.yuklenmis_meshler[parca_id] = mesh

                mesh = self.yuklenmis_meshler[parca_id]
                renk = tuple(parca['renk'])

                self.gorunum_3d.mesh_ekle(parca_id, mesh, renk=renk)
                yuklenen += 1

                # Ilerleme goster
                if i % 10 == 0:
                    self.statusBar().showMessage(f"Tum parcalar yukleniyor... {i}/{toplam}")
                    QApplication.processEvents()

            except Exception as e:
                print(f"Hata [{parca_id}]: {e}")

        self.gorunum_3d.kamerayi_sifirla()
        self.lbl_3d_bilgi.setText(f"{yuklenen}/{toplam} parca goruntulenyor")
        self.statusBar().showMessage(f"{yuklenen} parca yuklendi!")

        # 3D tab'ina gec
        self.orta_tabs.setCurrentIndex(0)

    def renk_sec(self):
        """Renk sec - 3D'de canli guncelle"""
        index = self.parca_listesi.currentRow()
        if index < 0:
            return

        parca = self.parcalar[index]

        # Mevcut renk
        r, g, b = parca['renk']
        mevcut_renk = QColor(int(r*255), int(g*255), int(b*255))

        renk = QColorDialog.getColor(mevcut_renk, self, "Parca Rengi Sec")
        if renk.isValid():
            # Rengi kaydet
            parca['renk'] = [renk.red()/255, renk.green()/255, renk.blue()/255]

            # Ornegi guncelle
            self.renk_ornek.setStyleSheet(
                f"background-color: {renk.name()}; border: 1px solid black;"
            )

            # 3D'de canli guncelle
            parca_id = parca['id']
            if parca_id in self.yuklenmis_meshler:
                self.gorunum_3d.mesh_rengini_ayarla(parca_id, tuple(parca['renk']))

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

        parca = self.parcalar[index]
        yanit = QMessageBox.question(self, "Emin misiniz?",
                                     f"{parca['isim']} parcasini silmek istediginizden emin misiniz?")
        if yanit == QMessageBox.StandardButton.Yes:
            # 3D'den kaldir
            parca_id = parca['id']
            if parca_id in self.yuklenmis_meshler:
                self.gorunum_3d.mesh_kaldir(parca_id)
                del self.yuklenmis_meshler[parca_id]

            del self.parcalar[index]
            self.parca_listesi.takeItem(index)
            self.lbl_toplam.setText(f"Toplam: {len(self.parcalar)} parca")

    def parcalari_filtrele(self):
        """Parca listesini filtrele"""
        arama_metni = self.txt_ara.text().lower()

        for i in range(self.parca_listesi.count()):
            item = self.parca_listesi.item(i)
            goster = arama_metni in item.text().lower()
            item.setHidden(not goster)

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

        # Kamera pozisyonu
        kamera_poz = adim['kamera_pozisyonu']
        self.txt_kamera_poz.setText(f"[{kamera_poz[0]}, {kamera_poz[1]}, {kamera_poz[2]}]")

        self.adim_duzenleme.setEnabled(True)
        self.btn_adim_sil.setEnabled(True)
        self.btn_adim_onizle.setEnabled(True)

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

        # Kamera pozisyonu parse et
        try:
            kamera_str = self.txt_kamera_poz.text().strip()
            kamera_str = kamera_str.replace('[', '').replace(']', '')
            kamera_liste = [float(x.strip()) for x in kamera_str.split(',')]
            if len(kamera_liste) == 3:
                adim['kamera_pozisyonu'] = kamera_liste
        except:
            pass

        # Listeyi guncelle
        self.adim_listesi.item(index).setText(f"{adim['adim_numarasi']}. {adim['baslik']}")

    def adim_onizle(self):
        """Secili adimin 3D onizlemesini goster"""
        index = self.adim_listesi.currentRow()
        if index < 0:
            return

        adim = self.adimlar[index]

        # Sahneyi temizle
        self.gorunum_3d.sahneyi_temizle()

        # Gorunur parcalari yukle
        gorunur_ids = adim['gorunur_parcalar']
        vurgulu_ids = adim['vurgulu_parcalar']

        if not gorunur_ids:
            QMessageBox.information(self, "Bilgi", "Bu adimda gorunur parca yok!")
            return

        yuklenen = 0

        for parca in self.parcalar:
            parca_id = parca['id']

            if parca_id in gorunur_ids:
                # Mesh yukle
                if parca_id not in self.yuklenmis_meshler:
                    try:
                        dosya_yolu = self.step_klasoru / parca['model_dosyasi']
                        mesh = self.model_yukleyici.model_yukle(dosya_yolu)
                        self.yuklenmis_meshler[parca_id] = mesh
                    except Exception as e:
                        print(f"Hata [{parca_id}]: {e}")
                        continue

                mesh = self.yuklenmis_meshler[parca_id]

                # Vurgulu mu?
                if parca_id in vurgulu_ids:
                    renk = (1.0, 1.0, 0.0)  # Sari
                else:
                    renk = tuple(parca['renk'])

                self.gorunum_3d.mesh_ekle(parca_id, mesh, renk=renk)
                yuklenen += 1

        # Kamera pozisyonunu ayarla
        kamera_poz = adim['kamera_pozisyonu']
        self.gorunum_3d.kamera_pozisyonunu_ayarla(kamera_poz, [0, 0, 0])

        self.lbl_3d_bilgi.setText(f"Adim {index+1}: {yuklenen} parca")
        self.statusBar().showMessage(f"Adim {index+1} onizlemesi yuklendi!")

        # 3D tab'ina gec
        self.orta_tabs.setCurrentIndex(0)

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

    def kamera_pozisyonu_kaydet(self):
        """Mevcut kamera pozisyonunu kaydet"""
        # VTK kameradan pozisyon al
        kamera = self.gorunum_3d.renderer.GetActiveCamera()
        pozisyon = kamera.GetPosition()

        # Secili adima kaydet
        index = self.adim_listesi.currentRow()
        if index >= 0:
            self.adimlar[index]['kamera_pozisyonu'] = list(pozisyon)
            self.txt_kamera_poz.setText(f"[{pozisyon[0]:.1f}, {pozisyon[1]:.1f}, {pozisyon[2]:.1f}]")
            QMessageBox.information(self, "Basarili",
                                   f"Kamera pozisyonu kaydedildi:\n{pozisyon}")
        else:
            QMessageBox.warning(self, "Uyari", "Once bir adim secin!")

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
                                   f"JSON dosyasi kaydedildi:\n{dosya}\n\n"
                                   f"Parcalar: {len(self.parcalar)}\n"
                                   f"Adimlar: {len(self.adimlar)}")
            self.statusBar().showMessage(f"JSON kaydedildi: {dosya}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"JSON kaydetme hatasi:\n{str(e)}")


def main():
    """Ana fonksiyon"""
    app = QApplication(sys.argv)
    app.setApplicationName("JSON Creator - 3D Onizlemeli")

    pencere = JSONCreatorGUI()
    pencere.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
