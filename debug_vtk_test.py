#!/usr/bin/env python3
"""
VTK Widget Test - Detaylı debug
"""
import sys
import traceback

print("=" * 70)
print("VTK WIDGET DEBUG TEST")
print("=" * 70)

try:
    print("\n1. PyQt6 import...")
    from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
    from PyQt6.QtCore import Qt
    print("   ✓ PyQt6 OK")

    print("\n2. VTK import...")
    import vtk
    print(f"   ✓ VTK OK - Versiyon: {vtk.vtkVersion.GetVTKVersion()}")

    print("\n3. VTK-Qt Interactor import...")
    from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
    print("   ✓ QVTKRenderWindowInteractor OK")

    print("\n4. QApplication oluşturuluyor...")
    uygulama = QApplication(sys.argv)
    print("   ✓ QApplication OK")

    print("\n5. Ana widget oluşturuluyor...")
    ana_widget = QWidget()
    ana_widget.setWindowTitle("VTK Test")
    ana_widget.setGeometry(100, 100, 800, 600)
    print("   ✓ Ana widget OK")

    print("\n6. Layout oluşturuluyor...")
    layout = QVBoxLayout(ana_widget)
    print("   ✓ Layout OK")

    print("\n7. QVTKRenderWindowInteractor oluşturuluyor...")
    vtk_widget = QVTKRenderWindowInteractor(ana_widget)
    print("   ✓ VTK widget oluşturuldu")

    print("\n8. Layout'a ekleniyor...")
    layout.addWidget(vtk_widget)
    print("   ✓ Layout'a eklendi")

    print("\n9. VTK Renderer oluşturuluyor...")
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0.2, 0.3, 0.4)
    print("   ✓ Renderer OK")

    print("\n10. Render Window alınıyor...")
    render_window = vtk_widget.GetRenderWindow()
    print("   ✓ Render window OK")

    print("\n11. Renderer ekleniyor...")
    render_window.AddRenderer(renderer)
    print("   ✓ Renderer eklendi")

    print("\n12. Interactor alınıyor...")
    interactor = render_window.GetInteractor()
    print("   ✓ Interactor OK")

    print("\n13. Interactor style ayarlanıyor...")
    style = vtk.vtkInteractorStyleTrackballCamera()
    interactor.SetInteractorStyle(style)
    print("   ✓ Style ayarlandı")

    print("\n14. Kamera ayarlanıyor...")
    kamera = renderer.GetActiveCamera()
    kamera.SetPosition(100, 100, 100)
    kamera.SetFocalPoint(0, 0, 0)
    kamera.SetViewUp(0, 0, 1)
    renderer.ResetCamera()
    print("   ✓ Kamera OK")

    print("\n15. Interactor Initialize ediliyor...")
    interactor.Initialize()
    print("   ✓ Initialize OK")

    print("\n16. Widget gösteriliyor...")
    ana_widget.show()
    print("   ✓ Widget gösterildi")

    print("\n17. Widget durumu kontrol ediliyor...")
    print(f"   Görünür: {ana_widget.isVisible()}")
    print(f"   Genişlik: {ana_widget.width()}")
    print(f"   Yükseklik: {ana_widget.height()}")

    print("\n" + "=" * 70)
    print("TÜM TESTLER BAŞARILI!")
    print("VTK penceresi açılmalı. Kapatmak için X'e tıklayın.")
    print("=" * 70 + "\n")

    sys.exit(uygulama.exec())

except Exception as e:
    print("\n" + "=" * 70)
    print("HATA BULUNDU!")
    print("=" * 70)
    print(f"\nHata Mesajı: {e}")
    print(f"\nHata Tipi: {type(e).__name__}")
    print("\nDetaylı Stack Trace:")
    print("-" * 70)
    traceback.print_exc()
    print("-" * 70)
    print("\nMuhtemel Çözümler:")
    print("1. VTK'nın OpenGL desteği eksik olabilir")
    print("2. Grafik sürücüleri güncellenmelidir")
    print("3. VTK'yı yeniden kurun: conda install -c conda-forge vtk -y")
    print("=" * 70)

    input("\nDevam etmek için Enter'a basın...")
    sys.exit(1)
