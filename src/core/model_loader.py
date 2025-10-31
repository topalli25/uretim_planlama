"""
3D model dosyalarını yükleyen modül
STL ve STEP formatlarını destekler
"""
import os
import trimesh
import numpy as np
from pathlib import Path


class ModelLoader:
    """3D model dosyalarını yükler ve işler"""

    def __init__(self):
        self.supported_formats = ['.stl', '.STL', '.step', '.stp', '.STEP', '.STP']

    def load_model(self, file_path):
        """
        3D model dosyasını yükle

        Args:
            file_path (str): Model dosyasının yolu

        Returns:
            trimesh.Trimesh: Yüklenmiş 3D model
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Model dosyası bulunamadı: {file_path}")

        if file_path.suffix not in self.supported_formats:
            raise ValueError(f"Desteklenmeyen dosya formatı: {file_path.suffix}")

        try:
            # trimesh ile modeli yükle
            mesh = trimesh.load(str(file_path))

            # Eğer Scene ise ilk mesh'i al
            if isinstance(mesh, trimesh.Scene):
                # Scene içindeki tüm geometrileri birleştir
                meshes = []
                for geom in mesh.geometry.values():
                    if isinstance(geom, trimesh.Trimesh):
                        meshes.append(geom)
                if meshes:
                    mesh = trimesh.util.concatenate(meshes)
                else:
                    raise ValueError("Scene içinde geçerli mesh bulunamadı")

            return mesh

        except Exception as e:
            raise Exception(f"Model yüklenirken hata: {str(e)}")

    def load_multiple_models(self, file_paths):
        """
        Birden fazla model dosyasını yükle

        Args:
            file_paths (list): Model dosyalarının yolları

        Returns:
            dict: {dosya_adı: mesh} sözlüğü
        """
        models = {}
        for file_path in file_paths:
            name = Path(file_path).stem
            try:
                models[name] = self.load_model(file_path)
            except Exception as e:
                print(f"Hata: {name} yüklenemedi - {str(e)}")

        return models

    def get_model_info(self, mesh):
        """
        Model hakkında bilgi döndür

        Args:
            mesh (trimesh.Trimesh): 3D model

        Returns:
            dict: Model bilgileri
        """
        return {
            'vertices_count': len(mesh.vertices),
            'faces_count': len(mesh.faces),
            'bounds': mesh.bounds.tolist(),
            'center': mesh.centroid.tolist(),
            'volume': mesh.volume,
            'surface_area': mesh.area
        }
