"""
Montaj adımlarını kontrol eden panel
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QTextEdit, QListWidget, QProgressBar,
                             QGroupBox)
from PyQt6.QtCore import Qt, pyqtSignal


class ControlPanel(QWidget):
    """Montaj kontrol paneli"""

    # Signals
    step_changed = pyqtSignal(int)  # Adım değiştiğinde
    part_selected = pyqtSignal(str)  # Parça seçildiğinde

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """UI elemanlarını oluştur"""
        layout = QVBoxLayout(self)

        # Başlık
        title = QLabel("Montaj Adımları")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # İlerleme çubuğu
        progress_group = QGroupBox("İlerleme")
        progress_layout = QVBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_label = QLabel("Adım 0 / 0")
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.progress_label)
        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)

        # Mevcut adım bilgisi
        step_group = QGroupBox("Mevcut Adım")
        step_layout = QVBoxLayout()

        self.step_title = QLabel("Adım başlığı")
        self.step_title.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.step_title.setWordWrap(True)

        self.step_description = QTextEdit()
        self.step_description.setReadOnly(True)
        self.step_description.setMaximumHeight(100)

        step_layout.addWidget(self.step_title)
        step_layout.addWidget(self.step_description)
        step_group.setLayout(step_layout)
        layout.addWidget(step_group)

        # Navigasyon butonları
        nav_layout = QHBoxLayout()

        self.btn_first = QPushButton("⏮ İlk")
        self.btn_prev = QPushButton("◀ Önceki")
        self.btn_next = QPushButton("Sonraki ▶")
        self.btn_last = QPushButton("Son ⏭")

        self.btn_first.clicked.connect(self.on_first_clicked)
        self.btn_prev.clicked.connect(self.on_prev_clicked)
        self.btn_next.clicked.connect(self.on_next_clicked)
        self.btn_last.clicked.connect(self.on_last_clicked)

        nav_layout.addWidget(self.btn_first)
        nav_layout.addWidget(self.btn_prev)
        nav_layout.addWidget(self.btn_next)
        nav_layout.addWidget(self.btn_last)

        layout.addLayout(nav_layout)

        # Adım listesi
        steps_group = QGroupBox("Tüm Adımlar")
        steps_layout = QVBoxLayout()
        self.steps_list = QListWidget()
        self.steps_list.currentRowChanged.connect(self.on_step_list_changed)
        steps_layout.addWidget(self.steps_list)
        steps_group.setLayout(steps_layout)
        layout.addWidget(steps_group)

        # Parça listesi
        parts_group = QGroupBox("Parçalar")
        parts_layout = QVBoxLayout()
        self.parts_list = QListWidget()
        self.parts_list.currentTextChanged.connect(self.on_part_selected)
        parts_layout.addWidget(self.parts_list)
        parts_group.setLayout(parts_layout)
        layout.addWidget(parts_group)

        # Stretch
        layout.addStretch()

    def update_step_info(self, step, current_index, total_steps):
        """
        Adım bilgilerini güncelle

        Args:
            step (dict): Adım bilgisi
            current_index (int): Mevcut adım indexi (0-based)
            total_steps (int): Toplam adım sayısı
        """
        if step:
            self.step_title.setText(step.get('title', 'Başlık yok'))
            self.step_description.setPlainText(step.get('description', 'Açıklama yok'))
        else:
            self.step_title.setText("Adım yok")
            self.step_description.setPlainText("")

        # İlerleme güncelle
        if total_steps > 0:
            progress = int(((current_index + 1) / total_steps) * 100)
            self.progress_bar.setValue(progress)
            self.progress_label.setText(f"Adım {current_index + 1} / {total_steps}")
        else:
            self.progress_bar.setValue(0)
            self.progress_label.setText("Adım 0 / 0")

        # Buton durumları
        self.btn_first.setEnabled(current_index > 0)
        self.btn_prev.setEnabled(current_index > 0)
        self.btn_next.setEnabled(current_index < total_steps - 1)
        self.btn_last.setEnabled(current_index < total_steps - 1)

        # Listede seç
        if 0 <= current_index < self.steps_list.count():
            self.steps_list.setCurrentRow(current_index)

    def load_steps(self, steps):
        """Adım listesini yükle"""
        self.steps_list.clear()
        for i, step in enumerate(steps):
            self.steps_list.addItem(f"{i+1}. {step.get('title', 'İsimsiz')}")

    def load_parts(self, parts):
        """Parça listesini yükle"""
        self.parts_list.clear()
        for part in parts:
            self.parts_list.addItem(f"{part.get('name', 'İsimsiz')} [{part.get('id')}]")

    def on_first_clicked(self):
        """İlk adıma git"""
        self.step_changed.emit(0)

    def on_prev_clicked(self):
        """Önceki adım"""
        self.step_changed.emit(-1)  # -1 = önceki

    def on_next_clicked(self):
        """Sonraki adım"""
        self.step_changed.emit(1)  # 1 = sonraki

    def on_last_clicked(self):
        """Son adıma git"""
        self.step_changed.emit(9999)  # Büyük sayı = son

    def on_step_list_changed(self, index):
        """Liste üzerinden adım değiştirildi"""
        if index >= 0:
            self.step_changed.emit(index + 100)  # +100 = direkt adım

    def on_part_selected(self, text):
        """Parça seçildi"""
        if text:
            # ID'yi ayıkla [id] formatından
            part_id = text.split('[')[-1].replace(']', '').strip()
            self.part_selected.emit(part_id)
