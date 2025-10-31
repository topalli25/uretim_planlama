"""
Montaj ve alt montaj yönetimi
"""
from pathlib import Path
from src.utils.helpers import load_json, save_json


class AssemblyManager:
    """Montaj bilgilerini yönetir"""

    def __init__(self, assemblies_dir='data/assemblies'):
        self.assemblies_dir = Path(assemblies_dir)
        self.current_assembly = None
        self.parts = {}

    def load_assembly(self, assembly_file):
        """
        Montaj JSON dosyasını yükle

        Assembly JSON formatı:
        {
            "name": "Ana Montaj",
            "description": "Ürün montajı",
            "parts": [
                {
                    "id": "part_001",
                    "name": "Gövde",
                    "model_file": "govde.stl",
                    "color": [1.0, 0.0, 0.0],
                    "visible": true
                }
            ],
            "steps": [...] # step_manager tarafından yönetilir
        }
        """
        assembly_path = self.assemblies_dir / assembly_file
        self.current_assembly = load_json(assembly_path)

        # Parçaları indexle
        self.parts = {part['id']: part for part in self.current_assembly.get('parts', [])}

        return self.current_assembly

    def get_part(self, part_id):
        """Belirli bir parçayı getir"""
        return self.parts.get(part_id)

    def get_all_parts(self):
        """Tüm parçaları getir"""
        return self.current_assembly.get('parts', [])

    def get_visible_parts(self):
        """Görünür parçaları getir"""
        return [part for part in self.get_all_parts() if part.get('visible', True)]

    def set_part_visibility(self, part_id, visible):
        """Parça görünürlüğünü ayarla"""
        if part_id in self.parts:
            self.parts[part_id]['visible'] = visible
            # Ana assembly'de de güncelle
            for part in self.current_assembly['parts']:
                if part['id'] == part_id:
                    part['visible'] = visible
                    break

    def get_assembly_info(self):
        """Montaj bilgilerini döndür"""
        if not self.current_assembly:
            return None

        return {
            'name': self.current_assembly.get('name', 'İsimsiz'),
            'description': self.current_assembly.get('description', ''),
            'total_parts': len(self.get_all_parts()),
            'visible_parts': len(self.get_visible_parts())
        }

    def create_sample_assembly(self, output_file='sample_assembly.json'):
        """Örnek montaj dosyası oluştur"""
        sample = {
            "name": "Örnek Montaj",
            "description": "Test amaçlı örnek montaj projesi",
            "parts": [
                {
                    "id": "part_001",
                    "name": "Taban",
                    "model_file": "taban.stl",
                    "color": [0.8, 0.8, 0.8],
                    "visible": True
                },
                {
                    "id": "part_002",
                    "name": "Gövde",
                    "model_file": "govde.stl",
                    "color": [0.2, 0.6, 1.0],
                    "visible": True
                },
                {
                    "id": "part_003",
                    "name": "Kapak",
                    "model_file": "kapak.stl",
                    "color": [1.0, 0.2, 0.2],
                    "visible": True
                }
            ],
            "steps": []
        }

        output_path = self.assemblies_dir / output_file
        save_json(sample, output_path)
        return output_path
