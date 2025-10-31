#!/usr/bin/env python3
"""
Test amaçlı basit 3D modeller oluşturur
"""
import trimesh
import numpy as np
from pathlib import Path


def create_sample_models():
    """Örnek STL dosyaları oluştur"""

    # Output dizini
    output_dir = Path(__file__).parent.parent / 'data' / 'models'
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Örnek 3D modeller oluşturuluyor...")

    # 1. Taban (Küp)
    print("1. Taban oluşturuluyor...")
    box = trimesh.creation.box(extents=[50, 50, 10])
    box.apply_translation([0, 0, -5])
    box.export(output_dir / 'taban.stl')

    # 2. Gövde (Silindir)
    print("2. Gövde oluşturuluyor...")
    cylinder = trimesh.creation.cylinder(radius=15, height=40)
    cylinder.apply_translation([0, 0, 20])
    cylinder.export(output_dir / 'govde.stl')

    # 3. Kapak (Küre)
    print("3. Kapak oluşturuluyor...")
    sphere = trimesh.creation.icosphere(subdivisions=3, radius=12)
    sphere.apply_translation([0, 0, 42])
    sphere.export(output_dir / 'kapak.stl')

    # 4. Ek parça 1 (Küçük küp)
    print("4. Ek parça 1 oluşturuluyor...")
    small_box1 = trimesh.creation.box(extents=[8, 8, 30])
    small_box1.apply_translation([20, 20, 15])
    small_box1.export(output_dir / 'destek_1.stl')

    # 5. Ek parça 2 (Küçük küp)
    print("5. Ek parça 2 oluşturuluyor...")
    small_box2 = trimesh.creation.box(extents=[8, 8, 30])
    small_box2.apply_translation([-20, -20, 15])
    small_box2.export(output_dir / 'destek_2.stl')

    print(f"\n✓ 5 adet örnek STL dosyası oluşturuldu:")
    print(f"  {output_dir}")
    print(f"  - taban.stl")
    print(f"  - govde.stl")
    print(f"  - kapak.stl")
    print(f"  - destek_1.stl")
    print(f"  - destek_2.stl")


if __name__ == '__main__':
    create_sample_models()
