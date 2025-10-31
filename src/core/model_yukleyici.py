"""
3D model dosyalarını yükleyen modül
STEP ve STL formatlarını destekler (STEP öncelikli)
"""
import os
import trimesh
import numpy as np
from pathlib import Path


class ModelYukleyici:
    """3D model dosyalarını yükler ve işler"""

    def __init__(self):
        # STEP formatı öncelikli, sonra STL
        self.desteklenen_formatlar = ['.step', '.stp', '.STEP', '.STP', '.stl', '.STL']

    def model_yukle(self, dosya_yolu):
        """
        3D model dosyasını yükle

        Args:
            dosya_yolu (str): Model dosyasının yolu

        Returns:
            trimesh.Trimesh: Yüklenmiş 3D model
        """
        dosya_yolu = Path(dosya_yolu)

        if not dosya_yolu.exists():
            raise FileNotFoundError(f"Model dosyası bulunamadı: {dosya_yolu}")

        if dosya_yolu.suffix not in self.desteklenen_formatlar:
            raise ValueError(f"Desteklenmeyen dosya formatı: {dosya_yolu.suffix}")

        try:
            # trimesh ile modeli yükle
            mesh = trimesh.load(str(dosya_yolu))

            # Eğer Scene ise ilk mesh'i al
            if isinstance(mesh, trimesh.Scene):
                # Scene içindeki tüm geometrileri birleştir
                meshler = []
                for geometri in mesh.geometry.values():
                    if isinstance(geometri, trimesh.Trimesh):
                        meshler.append(geometri)
                if meshler:
                    mesh = trimesh.util.concatenate(meshler)
                else:
                    raise ValueError("Scene içinde geçerli mesh bulunamadı")

            return mesh

        except Exception as e:
            raise Exception(f"Model yüklenirken hata: {str(e)}")

    def coklu_model_yukle(self, dosya_yollari):
        """
        Birden fazla model dosyasını yükle

        Args:
            dosya_yollari (list): Model dosyalarının yolları

        Returns:
            dict: {dosya_adi: mesh} sözlüğü
        """
        modeller = {}
        for dosya_yolu in dosya_yollari:
            isim = Path(dosya_yolu).stem
            try:
                modeller[isim] = self.model_yukle(dosya_yolu)
            except Exception as e:
                print(f"Hata: {isim} yüklenemedi - {str(e)}")

        return modeller

    def model_bilgisi_al(self, mesh):
        """
        Model hakkında bilgi döndür

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
