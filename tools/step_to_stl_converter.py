#!/usr/bin/env python3
"""
STEP to STL Converter - Toplu dosya donusturucu

STEP dosyalarini STL formatina donusturur.
Birden fazla yontem dener:
1. FreeCAD (en iyi kalite)
2. trimesh + pyassimp (orta kalite)
3. Online API (internet gerekir)
"""
import sys
import os
from pathlib import Path
import argparse


def freecad_ile_donustur(step_dosya, stl_dosya):
    """FreeCAD kullanarak STEP'i STL'ye donustur"""
    try:
        import FreeCAD
        import Mesh
        import Import

        print(f"FreeCAD ile donusturuluyor: {step_dosya.name}")

        # STEP yukle
        doc = FreeCAD.newDocument()
        Import.insert(str(step_dosya), doc.Name)

        # Mesh'e cevir
        for obj in doc.Objects:
            if hasattr(obj, 'Shape'):
                mesh = Mesh.Mesh(obj.Shape.tessellate(0.1))
                mesh.write(str(stl_dosya))
                print(f"  Basarili: {stl_dosya.name}")
                return True

        return False

    except ImportError:
        return False
    except Exception as e:
        print(f"  FreeCAD hatasi: {e}")
        return False


def trimesh_ile_donustur(step_dosya, stl_dosya):
    """trimesh + pyassimp kullanarak donustur"""
    try:
        import trimesh

        print(f"trimesh ile donusturuluyor: {step_dosya.name}")

        # STEP yukle
        mesh = trimesh.load(str(step_dosya))

        # Scene ise birlestir
        if isinstance(mesh, trimesh.Scene):
            meshler = []
            for geometri in mesh.geometry.values():
                if isinstance(geometri, trimesh.Trimesh):
                    meshler.append(geometri)
            if meshler:
                mesh = trimesh.util.concatenate(meshler)

        # STL kaydet
        mesh.export(str(stl_dosya))
        print(f"  Basarili: {stl_dosya.name}")
        return True

    except Exception as e:
        print(f"  trimesh hatasi: {e}")
        return False


def manuel_donusturme_kilavuzu():
    """Kullaniciya manuel donusturme talimlari ver"""
    print("\n" + "="*70)
    print("MANUEL DONUSTURME KILAVUZU")
    print("="*70)
    print("""
STEP dosyalarinizi STL formatina donusturmek icin:

YONTEM 1: SolidWorks
  1. SolidWorks'te parcayi/montaji acin
  2. File > Save As > STL (*.stl)
  3. Options:
     - Resolution: Fine veya Custom
     - Units: Millimeters
     - Format: Binary (daha kucuk dosya)
  4. Save

YONTEM 2: FreeCAD (Ucretsiz)
  1. FreeCAD'i indirin: https://www.freecad.org/
  2. File > Open > STEP dosyasini secin
  3. Parcayi secin
  4. File > Export > Mesh Formats (STL)
  5. Save

YONTEM 3: Online Donusturucu (Hizli)
  - https://www.convertonline.io/convert/step-to-stl
  - https://products.aspose.app/3d/conversion/step-to-stl

  NOT: Gizli/ozel projeler icin online kullanmayin!

YONTEM 4: FreeCAD Toplu Donusturucu
  Bu script'i FreeCAD yuklu bilgisayarda calistirin:
  python step_to_stl_converter.py --freecad <klasor>
""")
    print("="*70)


def toplu_donustur(klasor, yontem='auto'):
    """Klasordeki tum STEP dosyalarini STL'ye donustur"""
    klasor = Path(klasor)

    if not klasor.exists():
        print(f"HATA: Klasor bulunamadi: {klasor}")
        return

    # STEP dosyalarini bul
    step_dosyalar = list(klasor.glob("*.step")) + \
                    list(klasor.glob("*.stp")) + \
                    list(klasor.glob("*.STEP")) + \
                    list(klasor.glob("*.STP"))

    if not step_dosyalar:
        print(f"HATA: Klasorde STEP dosyasi bulunamadi: {klasor}")
        return

    print(f"\nBulunan STEP dosyasi: {len(step_dosyalar)}")
    print(f"Klasor: {klasor}\n")

    basarili = 0
    basarisiz = 0
    atlanan = 0

    for step_dosya in sorted(step_dosyalar):
        stl_dosya = step_dosya.with_suffix('.stl')

        # STL zaten varsa atla
        if stl_dosya.exists():
            print(f"Atlandi (zaten var): {step_dosya.name}")
            atlanan += 1
            continue

        # Donusturmeyi dene
        donustu = False

        if yontem in ['auto', 'freecad']:
            donustu = freecad_ile_donustur(step_dosya, stl_dosya)

        if not donustu and yontem in ['auto', 'trimesh']:
            donustu = trimesh_ile_donustur(step_dosya, stl_dosya)

        if donustu:
            basarili += 1
        else:
            basarisiz += 1
            print(f"BASARISIZ: {step_dosya.name}")

    # Ozet
    print("\n" + "="*70)
    print("DONUSTURME OZETI")
    print("="*70)
    print(f"Toplam dosya:    {len(step_dosyalar)}")
    print(f"Basarili:        {basarili}")
    print(f"Basarisiz:       {basarisiz}")
    print(f"Atlanan (var):   {atlanan}")
    print("="*70)

    if basarisiz > 0:
        print("\nBASARISIZ dosyalar manuel olarak donusturulmeli!")
        manuel_donusturme_kilavuzu()


def main():
    """Ana fonksiyon"""
    parser = argparse.ArgumentParser(
        description='STEP dosyalarini STL formatina donusturur',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
ORNEKLER:
  # Klasordeki tum STEP'leri donustur (otomatik yontem)
  python step_to_stl_converter.py /path/to/step/klasoru

  # Sadece FreeCAD kullan
  python step_to_stl_converter.py --freecad /path/to/klasor

  # Sadece trimesh kullan
  python step_to_stl_converter.py --trimesh /path/to/klasor

  # Manuel kilavuz goster
  python step_to_stl_converter.py --help-manual
        """
    )

    parser.add_argument('klasor', nargs='?', help='STEP dosyalarinin bulundugu klasor')
    parser.add_argument('--freecad', metavar='KLASOR', help='Sadece FreeCAD kullan')
    parser.add_argument('--trimesh', metavar='KLASOR', help='Sadece trimesh kullan')
    parser.add_argument('--help-manual', action='store_true', help='Manuel donusturme kilavuzunu goster')

    args = parser.parse_args()

    # Manuel kilavuz
    if args.help_manual:
        manuel_donusturme_kilavuzu()
        return

    # Klasor belirleme
    klasor = None
    yontem = 'auto'

    if args.freecad:
        klasor = args.freecad
        yontem = 'freecad'
    elif args.trimesh:
        klasor = args.trimesh
        yontem = 'trimesh'
    elif args.klasor:
        klasor = args.klasor
    else:
        parser.print_help()
        print("\n")
        manuel_donusturme_kilavuzu()
        return

    # Donusturme yap
    toplu_donustur(klasor, yontem)


if __name__ == '__main__':
    main()
