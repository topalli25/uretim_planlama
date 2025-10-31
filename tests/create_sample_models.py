#!/usr/bin/env python3
"""
Test amaçlı basit 3D modeller oluşturur (STEP ve STL formatında)
"""
import trimesh
import numpy as np
from pathlib import Path


def ornek_modeller_olustur():
    """Örnek STEP ve STL dosyaları oluştur"""

    # Output dizini
    cikti_dizini = Path(__file__).parent.parent / 'data' / 'models'
    cikti_dizini.mkdir(parents=True, exist_ok=True)

    print("Örnek 3D modeller oluşturuluyor...")
    print("Not: STEP formatı öncelikli, STL yedek olarak oluşturuluyor.\n")

    # 1. Taban (Küp)
    print("1. Taban oluşturuluyor...")
    kutu = trimesh.creation.box(extents=[50, 50, 10])
    kutu.apply_translation([0, 0, -5])
    kutu.export(cikti_dizini / 'taban.step')  # STEP öncelikli
    kutu.export(cikti_dizini / 'taban.stl')   # STL yedek

    # 2. Gövde (Silindir)
    print("2. Gövde oluşturuluyor...")
    silindir = trimesh.creation.cylinder(radius=15, height=40)
    silindir.apply_translation([0, 0, 20])
    silindir.export(cikti_dizini / 'govde.step')
    silindir.export(cikti_dizini / 'govde.stl')

    # 3. Kapak (Küre)
    print("3. Kapak oluşturuluyor...")
    kure = trimesh.creation.icosphere(subdivisions=3, radius=12)
    kure.apply_translation([0, 0, 42])
    kure.export(cikti_dizini / 'kapak.step')
    kure.export(cikti_dizini / 'kapak.stl')

    # 4. Ek parça 1 (Küçük küp)
    print("4. Destek 1 oluşturuluyor...")
    kucuk_kutu1 = trimesh.creation.box(extents=[8, 8, 30])
    kucuk_kutu1.apply_translation([20, 20, 15])
    kucuk_kutu1.export(cikti_dizini / 'destek_1.step')
    kucuk_kutu1.export(cikti_dizini / 'destek_1.stl')

    # 5. Ek parça 2 (Küçük küp)
    print("5. Destek 2 oluşturuluyor...")
    kucuk_kutu2 = trimesh.creation.box(extents=[8, 8, 30])
    kucuk_kutu2.apply_translation([-20, -20, 15])
    kucuk_kutu2.export(cikti_dizini / 'destek_2.step')
    kucuk_kutu2.export(cikti_dizini / 'destek_2.stl')

    print(f"\n✓ 5 adet örnek model oluşturuldu (STEP + STL):")
    print(f"  Dizin: {cikti_dizini}")
    print(f"\n  STEP Dosyaları (Öncelikli):")
    print(f"  - taban.step")
    print(f"  - govde.step")
    print(f"  - kapak.step")
    print(f"  - destek_1.step")
    print(f"  - destek_2.step")
    print(f"\n  STL Dosyaları (Yedek):")
    print(f"  - taban.stl")
    print(f"  - govde.stl")
    print(f"  - kapak.stl")
    print(f"  - destek_1.stl")
    print(f"  - destek_2.stl")


if __name__ == '__main__':
    ornek_modeller_olustur()
