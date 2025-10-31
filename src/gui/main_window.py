"""
Ana uygulama penceresi
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                             QMenuBar, QMenu, QFileDialog, QMessageBox,
                             QStatusBar, QSplitter)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

from src.gui.viewer_widget import VTKViewerWidget
from src.gui.control_panel import ControlPanel
from src.core.model_loader import ModelLoader
from src.core.assembly_manager import AssemblyManager
from src.core.step_manager import StepManager
from src.utils.helpers import get_config, get_project_root


class MainWindow(QMainWindow):
    """Ana uygulama penceresi"""

    def __init__(self):
        super().__init__()

        # Config yükle
        self.config = get_config()

        # Modüller
        self.model_loader = ModelLoader()
        self.assembly_manager = AssemblyManager()
        self.step_manager = StepManager()
        self.loaded_models = {}  # part_id: mesh

        # UI oluştur
        self.init_ui()

    def init_ui(self):
        """UI elemanlarını oluştur"""
        self.setWindowTitle(self.config['app']['name'])
        self.setGeometry(100, 100,
                        self.config['app']['window_width'],
                        self.config['app']['window_height'])

        # Merkezi widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Ana layout
        main_layout = QHBoxLayout(central_widget)

        # Splitter (3D viewer ve kontrol paneli)
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # 3D Viewer
        self.viewer = VTKViewerWidget()
        splitter.addWidget(self.viewer)

        # Kontrol Paneli
        self.control_panel = ControlPanel()
        self.control_panel.setMaximumWidth(400)
        self.control_panel.setMinimumWidth(300)
        self.control_panel.step_changed.connect(self.on_step_changed)
        self.control_panel.part_selected.connect(self.on_part_selected)
        splitter.addWidget(self.control_panel)

        # Splitter oranı (70% viewer, 30% panel)
        splitter.setStretchFactor(0, 7)
        splitter.setStretchFactor(1, 3)

        main_layout.addWidget(splitter)

        # Menü bar
        self.create_menu_bar()

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Hazır")

    def create_menu_bar(self):
        """Menü çubuğunu oluştur"""
        menubar = self.menuBar()

        # Dosya menüsü
        file_menu = menubar.addMenu("Dosya")

        open_action = QAction("Montaj Aç...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_assembly)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        exit_action = QAction("Çıkış", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Görünüm menüsü
        view_menu = menubar.addMenu("Görünüm")

        reset_camera_action = QAction("Kamerayı Sıfırla", self)
        reset_camera_action.setShortcut("R")
        reset_camera_action.triggered.connect(self.viewer.reset_camera)
        view_menu.addAction(reset_camera_action)

        fullscreen_action = QAction("Tam Ekran", self)
        fullscreen_action.setShortcut("F11")
        fullscreen_action.setCheckable(True)
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        view_menu.addAction(fullscreen_action)

        # Yardım menüsü
        help_menu = menubar.addMenu("Yardım")

        about_action = QAction("Hakkında", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def open_assembly(self):
        """Montaj dosyası aç"""
        project_root = get_project_root()
        assemblies_dir = project_root / self.config['paths']['assemblies_dir']

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Montaj Dosyası Seç",
            str(assemblies_dir),
            "JSON Dosyaları (*.json)"
        )

        if file_path:
            try:
                self.load_assembly(file_path)
                self.status_bar.showMessage(f"Montaj yüklendi: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Montaj yüklenemedi:\n{str(e)}")

    def load_assembly(self, assembly_file):
        """
        Montaj dosyasını yükle ve görselleştir

        Args:
            assembly_file (str): Montaj JSON dosyasının yolu
        """
        # Montaj bilgilerini yükle
        assembly_data = self.assembly_manager.load_assembly(assembly_file)

        # Adımları yükle
        self.step_manager.load_steps(assembly_data.get('steps', []))

        # 3D modelleri yükle
        self.load_models()

        # UI'ı güncelle
        self.control_panel.load_steps(self.step_manager.get_all_steps())
        self.control_panel.load_parts(self.assembly_manager.get_all_parts())

        # İlk adımı göster
        if self.step_manager.get_step_count() > 0:
            self.update_step_view()

        self.status_bar.showMessage(
            f"Montaj yüklendi: {assembly_data['name']} "
            f"({len(self.loaded_models)} parça)"
        )

    def load_models(self):
        """Montajdaki tüm 3D modelleri yükle"""
        project_root = get_project_root()
        models_dir = project_root / self.config['paths']['models_dir']

        self.viewer.clear_scene()
        self.loaded_models.clear()

        for part in self.assembly_manager.get_all_parts():
            part_id = part['id']
            model_file = part['model_file']
            color = tuple(part.get('color', [0.8, 0.8, 0.8]))

            try:
                # Model dosyasını yükle
                model_path = models_dir / model_file
                mesh = self.model_loader.load_model(model_path)
                self.loaded_models[part_id] = mesh

                # Viewer'a ekle
                self.viewer.add_mesh(part_id, mesh, color=color)

                # Görünürlük ayarla
                visible = part.get('visible', True)
                self.viewer.set_mesh_visibility(part_id, visible)

            except Exception as e:
                print(f"Model yüklenemedi [{part_id}]: {str(e)}")

        self.viewer.reset_camera()

    def update_step_view(self):
        """Mevcut adıma göre görünümü güncelle"""
        current_step = self.step_manager.get_current_step()
        current_index = self.step_manager.current_step_index
        total_steps = self.step_manager.get_step_count()

        # Kontrol panelini güncelle
        self.control_panel.update_step_info(current_step, current_index, total_steps)

        if not current_step:
            return

        # Parça görünürlüklerini güncelle
        visible_parts = current_step.get('visible_parts', [])
        for part_id in self.loaded_models.keys():
            self.viewer.set_mesh_visibility(part_id, part_id in visible_parts)

        # Vurgulanan parçalar
        highlight_parts = current_step.get('highlight_parts', [])
        for part_id in self.loaded_models.keys():
            if part_id in highlight_parts:
                self.viewer.highlight_mesh(part_id, True)
            else:
                # Orijinal renge dön
                part = self.assembly_manager.get_part(part_id)
                if part:
                    color = tuple(part.get('color', [0.8, 0.8, 0.8]))
                    self.viewer.set_mesh_color(part_id, color)

        # Kamera pozisyonu
        camera_pos = current_step.get('camera_position')
        if camera_pos:
            self.viewer.set_camera_position(camera_pos, [0, 0, 0])

    def on_step_changed(self, value):
        """Adım değiştirildiğinde"""
        if value == -1:
            # Önceki
            self.step_manager.previous_step()
        elif value == 1:
            # Sonraki
            self.step_manager.next_step()
        elif value == 0:
            # İlk
            self.step_manager.go_to_step(1)
        elif value == 9999:
            # Son
            self.step_manager.go_to_step(self.step_manager.get_step_count())
        elif value >= 100:
            # Direkt adım (liste seçimi)
            self.step_manager.go_to_step(value - 99)

        self.update_step_view()

    def on_part_selected(self, part_id):
        """Parça seçildiğinde"""
        # Parçayı vurgula
        for pid in self.loaded_models.keys():
            if pid == part_id:
                self.viewer.highlight_mesh(pid, True)
            else:
                part = self.assembly_manager.get_part(pid)
                if part:
                    color = tuple(part.get('color', [0.8, 0.8, 0.8]))
                    self.viewer.set_mesh_color(pid, color)

    def toggle_fullscreen(self, checked):
        """Tam ekran modunu aç/kapat"""
        if checked:
            self.showFullScreen()
        else:
            self.showNormal()

    def show_about(self):
        """Hakkında diyaloğu"""
        QMessageBox.about(
            self,
            "Hakkında",
            f"{self.config['app']['name']}\n"
            f"Versiyon: {self.config['app']['version']}\n\n"
            "3D montaj kılavuzu uygulaması\n"
            "SolidWorks CAD dosyalarından oluşturulan montaj talimatları"
        )

    def closeEvent(self, event):
        """Pencere kapatıldığında"""
        reply = QMessageBox.question(
            self,
            'Çıkış',
            'Uygulamadan çıkmak istediğinize emin misiniz?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
