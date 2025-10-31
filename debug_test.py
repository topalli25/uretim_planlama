#!/usr/bin/env python3
"""
Debug test - Adım adım kontrol
"""
import sys
import traceback

print("=" * 70)
print("DEBUG TEST BAŞLIYOR")
print("=" * 70)

try:
    print("\n1. PyQt6 import ediliyor...")
    from PyQt6.QtWidgets import QApplication
    print("   ✓ PyQt6 OK")

    print("\n2. VTK import ediliyor...")
    import vtk
    print("   ✓ VTK OK")

    print("\n3. VTK-Qt entegrasyonu kontrol ediliyor...")
    from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
    print("   ✓ VTK-Qt OK")

    print("\n4. Config dosyası okunuyor...")
    from src.utils.yardimcilar import konfig_al
    konfig = konfig_al()
    print(f"   ✓ Config yüklendi: {konfig['app']['name']}")

    print("\n5. Ana pencere sınıfı import ediliyor...")
    from src.gui.ana_pencere import AnaPencere
    print("   ✓ AnaPencere sınıfı OK")

    print("\n6. QApplication oluşturuluyor...")
    uygulama = QApplication(sys.argv)
    print("   ✓ QApplication oluşturuldu")

    print("\n7. Ana pencere oluşturuluyor...")
    pencere = AnaPencere()
    print("   ✓ Ana pencere oluşturuldu")

    print("\n8. Pencere gösteriliyor...")
    pencere.show()
    print("   ✓ Pencere show() çağrıldı")

    print("\n9. Pencere görünür mü kontrol ediliyor...")
    print(f"   Görünürlük: {pencere.isVisible()}")
    print(f"   Genişlik: {pencere.width()}")
    print(f"   Yükseklik: {pencere.height()}")

    print("\n" + "=" * 70)
    print("TÜM KONTROLLER BAŞARILI!")
    print("Şimdi uygulama döngüsü başlıyor...")
    print("Pencereyi kapatmak için X'e tıklayın")
    print("=" * 70 + "\n")

    sys.exit(uygulama.exec())

except Exception as e:
    print("\n" + "=" * 70)
    print("HATA BULUNDU!")
    print("=" * 70)
    print(f"\nHata: {e}")
    print("\nDetaylı hata:")
    traceback.print_exc()
    print("=" * 70)
    sys.exit(1)
