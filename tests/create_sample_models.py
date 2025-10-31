#!/usr/bin/env python3
"""
Test amaçlı basit 3D modeller oluşturur (STL formatında)
NOT: Gerçek projede SolidWorks'ten STEP dosyaları kullanılacak
"""
import trimesh
import numpy as np
from pathlib import Path


def ornek_modeller_olustur():
    """Örnek STL dosyaları oluştur (STEP export için pythonocc gerekli)"""

    # Output dizini
    cikti_dizini = Path(__file__).parent.parent / 'data' / 'models'
    cikti_dizini.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("Örnek 3D modeller oluşturuluyor (STL formatında)...")
    print("=" * 70)
    print("\nNOT: Bu test dosyalarıdır. Gerçek projenizde SolidWorks'ten")
    print("     STEP formatında (.step veya .stp) dosyaları export edin.")
    print("     Uygulama STEP formatını öncelikli olarak destekler.\n")

    # 1. Taban (Küp)
    print("1. Taban oluşturuluyor...")
    kutu = trimesh.creation.box(extents=[50, 50, 10])
    kutu.apply_translation([0, 0, -5])
    kutu.export(cikti_dizini / 'taban.stl')

    # 2. Gövde (Silindir)
    print("2. Gövde oluşturuluyor...")
    silindir = trimesh.creation.cylinder(radius=15, height=40)
    silindir.apply_translation([0, 0, 20])
    silindir.export(cikti_dizini / 'govde.stl')

    # 3. Kapak (Küre)
    print("3. Kapak oluşturuluyor...")
    kure = trimesh.creation.icosphere(subdivisions=3, radius=12)
    kure.apply_translation([0, 0, 42])
    kure.export(cikti_dizini / 'kapak.stl')

    # 4. Ek parça 1 (Küçük küp)
    print("4. Destek 1 oluşturuluyor...")
    kucuk_kutu1 = trimesh.creation.box(extents=[8, 8, 30])
    kucuk_kutu1.apply_translation([20, 20, 15])
    kucuk_kutu1.export(cikti_dizini / 'destek_1.stl')

    # 5. Ek parça 2 (Küçük küp)
    print("5. Destek 2 oluşturuluyor...")
    kucuk_kutu2 = trimesh.creation.box(extents=[8, 8, 30])
    kucuk_kutu2.apply_translation([-20, -20, 15])
    kucuk_kutu2.export(cikti_dizini / 'destek_2.stl')

    print(f"\n{'='*70}")
    print(f"✓ 5 adet örnek STL dosyası oluşturuldu")
    print(f"{'='*70}")
    print(f"\nDizin: {cikti_dizini}")
    print(f"\nOluşturulan Dosyalar:")
    print(f"  - taban.stl")
    print(f"  - govde.stl")
    print(f"  - kapak.stl")
    print(f"  - destek_1.stl")
    print(f"  - destek_2.stl")
    print(f"\n{'='*70}")
    print("GERÇEK PROJE İÇİN:")
    print(f"{'='*70}")
    print("1. SolidWorks'te parçalarınızı açın")
    print("2. File → Save As → STEP (*.step) formatını seçin")
    print("3. AP214 veya AP203 protokolünü seçin")
    print("4. data/models/ klasörüne kaydedin")
    print("5. JSON dosyasında 'model_dosyasi' alanını güncelleyin")
    print("   Örnek: 'model_dosyasi': 'parca.step'")
    print(f"{'='*70}\n")


if __name__ == '__main__':
    ornek_modeller_olustur()
