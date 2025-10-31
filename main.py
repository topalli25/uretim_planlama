#!/usr/bin/env python3
"""
3D Montaj Kılavuzu Uygulaması
Ana giriş noktası
"""
import sys
from PyQt6.QtWidgets import QApplication
from src.gui.main_window import MainWindow


def main():
    """Ana fonksiyon"""
    # Qt uygulaması
    app = QApplication(sys.argv)
    app.setApplicationName("3D Montaj Kılavuzu")
    app.setOrganizationName("Üretim Planlama")

    # Ana pencere
    window = MainWindow()
    window.show()

    # Uygulama döngüsü
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
