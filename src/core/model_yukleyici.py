"""
3D model dosyalarini yukleyen modul
STEP ve STL formatlarini destekler (STEP oncelikli)
"""
import os
import trimesh
import numpy as np
from pathlib import Path


class ModelYukleyici:
    """3D model dosyalarini yukler ve isler"""

    def __init__(self):
        # STEP formati oncelikli, sonra STL
        self.desteklenen_formatlar = ['.step', '.stp', '.STEP', '.STP', '.stl', '.STL']

    def model_yukle(self, dosya_yolu):
        """
        3D model dosyasini yukle

        Args:
            dosya_yolu (str): Model dosyasinin yolu

        Returns:
            trimesh.Trimesh: Yuklenmis 3D model
        """
        dosya_yolu = Path(dosya_yolu)

        if not dosya_yolu.exists():
            raise FileNotFoundError(f"Model dosyasi bulunamadi: {dosya_yolu}")

        if dosya_yolu.suffix not in self.desteklenen_formatlar:
            raise ValueError(f"Desteklenmeyen dosya formati: {dosya_yolu.suffix}")

        # STEP dosyasi ise once STL alternatifi var mi kontrol et
        uzanti = dosya_yolu.suffix.lower()
        if uzanti in ['.step', '.stp']:
            stl_alternatif = dosya_yolu.with_suffix('.stl')
            if stl_alternatif.exists():
                print(f"STEP yerine STL alternatifi kullaniliyor: {stl_alternatif.name}")
                dosya_yolu = stl_alternatif
                uzanti = '.stl'

        try:
            # trimesh ile modeli yukle
            mesh = trimesh.load(str(dosya_yolu))

            # Eger Scene ise ilk mesh'i al
            if isinstance(mesh, trimesh.Scene):
                # Scene icindeki tum geometrileri birlestir
                meshler = []
                for geometri in mesh.geometry.values():
                    if isinstance(geometri, trimesh.Trimesh):
                        meshler.append(geometri)
                if meshler:
                    mesh = trimesh.util.concatenate(meshler)
                else:
                    raise ValueError("Scene icinde gecerli mesh bulunamadi")

            return mesh

        except Exception as e:
            hata_mesaji = str(e)

            # STEP dosyasi yuklenemiyorsa ozel hata mesaji
            if uzanti in ['.step', '.stp'] and 'not supported' in hata_mesaji.lower():
                raise Exception(
                    f"STEP dosyasi yuklenemedi: {dosya_yolu.name}\n\n"
                    f"COZUM 1: STL'ye donusturun\n"
                    f"- SolidWorks'te: File > Save As > STL\n"
                    f"- FreeCAD: File > Export > Mesh Formats (STL)\n\n"
                    f"COZUM 2: Ek kutuphaneler yukleyin:\n"
                    f"pip install trimesh[easy] pyassimp\n\n"
                    f"Orijinal hata: {hata_mesaji}"
                )

            raise Exception(f"Model yuklenirken hata: {hata_mesaji}")

    def coklu_model_yukle(self, dosya_yollari):
        """
        Birden fazla model dosyasini yukle

        Args:
            dosya_yollari (list): Model dosyalarinin yollari

        Returns:
            dict: {dosya_adi: mesh} sozlugu
        """
        modeller = {}
        for dosya_yolu in dosya_yollari:
            isim = Path(dosya_yolu).stem
            try:
                modeller[isim] = self.model_yukle(dosya_yolu)
            except Exception as e:
                print(f"Hata: {isim} yuklenemedi - {str(e)}")

        return modeller

    def model_bilgisi_al(self, mesh):
        """
        Model hakkinda bilgi dondur

        Args:
            mesh (trimesh.Trimesh): 3D model

        Returns:
            dict: Model bilgileri
        """
        return {
            'nokta_sayisi': len(mesh.vertices),
            'yuzey_sayisi': len(mesh.faces),
            'sinirlar': mesh.bounds.tolist(),
            'merkez': mesh.centroid.tolist(),
            'hacim': mesh.volume,
            'yuzey_alani': mesh.area
        }
