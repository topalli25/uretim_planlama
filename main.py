#!/usr/bin/env python3
"""
3D Montaj Kılavuzu Uygulaması
Ana giriş noktası
"""
import sys
from PyQt6.QtWidgets import QApplication
from src.gui.ana_pencere import AnaPencere


def main():
    """Ana fonksiyon"""
    # Qt uygulaması
    uygulama = QApplication(sys.argv)
    uygulama.setApplicationName("3D Montaj Kılavuzu")
    uygulama.setOrganizationName("Üretim Planlama")

    # Ana pencere
    pencere = AnaPencere()
    pencere.show()

    # Uygulama döngüsü
    sys.exit(uygulama.exec())


if __name__ == '__main__':
    main()
