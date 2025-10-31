#!/usr/bin/env python3
"""
3D Montaj Kilavuzu Uygulamasi
Ana giris noktasi
"""
import sys
from PyQt6.QtWidgets import QApplication
from src.gui.ana_pencere import AnaPencere


def main():
    """Ana fonksiyon"""
    # Qt uygulamasi
    uygulama = QApplication(sys.argv)
    uygulama.setApplicationName("3D Montaj Kilavuzu")
    uygulama.setOrganizationName("Uretim Planlama")

    # Ana pencere
    pencere = AnaPencere()
    pencere.show()

    # Uygulama dongusu
    sys.exit(uygulama.exec())


if __name__ == '__main__':
    main()
