"""
Montaj adımlarını yönetir
"""


class StepManager:
    """Montaj adımlarını kontrol eder"""

    def __init__(self, assembly_data=None):
        self.assembly_data = assembly_data
        self.steps = []
        self.current_step_index = 0

        if assembly_data:
            self.load_steps(assembly_data.get('steps', []))

    def load_steps(self, steps):
        """
        Adımları yükle

        Adım formatı:
        {
            "step_number": 1,
            "title": "Tabanı yerleştir",
            "description": "Taban parçasını iş tezgahına sabitle",
            "visible_parts": ["part_001"],
            "highlight_parts": ["part_001"],
            "camera_position": [0, 0, 100],
            "duration": 30
        }
        """
        self.steps = steps
        self.current_step_index = 0

    def get_current_step(self):
        """Mevcut adımı döndür"""
        if 0 <= self.current_step_index < len(self.steps):
            return self.steps[self.current_step_index]
        return None

    def next_step(self):
        """Sonraki adıma geç"""
        if self.current_step_index < len(self.steps) - 1:
            self.current_step_index += 1
            return True
        return False

    def previous_step(self):
        """Önceki adıma geç"""
        if self.current_step_index > 0:
            self.current_step_index -= 1
            return True
        return False

    def go_to_step(self, step_number):
        """Belirli bir adıma git (1-based index)"""
        index = step_number - 1
        if 0 <= index < len(self.steps):
            self.current_step_index = index
            return True
        return False

    def get_step_count(self):
        """Toplam adım sayısı"""
        return len(self.steps)

    def get_progress(self):
        """İlerleme yüzdesi (0-100)"""
        if len(self.steps) == 0:
            return 0
        return int((self.current_step_index / len(self.steps)) * 100)

    def is_first_step(self):
        """İlk adımda mıyız?"""
        return self.current_step_index == 0

    def is_last_step(self):
        """Son adımda mıyız?"""
        return self.current_step_index == len(self.steps) - 1

    def get_all_steps(self):
        """Tüm adımları döndür"""
        return self.steps

    def create_sample_steps(self):
        """Örnek adımlar oluştur"""
        return [
            {
                "step_number": 1,
                "title": "Adım 1: Tabanı Hazırla",
                "description": "Taban parçasını alın ve iş tezgahına yerleştirin.",
                "visible_parts": ["part_001"],
                "highlight_parts": ["part_001"],
                "camera_position": [0, 0, 100],
                "duration": 30
            },
            {
                "step_number": 2,
                "title": "Adım 2: Gövdeyi Takın",
                "description": "Gövde parçasını taban üzerine yerleştirin ve 4 adet M6 cıvata ile sabitleyin.",
                "visible_parts": ["part_001", "part_002"],
                "highlight_parts": ["part_002"],
                "camera_position": [50, 50, 100],
                "duration": 60
            },
            {
                "step_number": 3,
                "title": "Adım 3: Kapağı Kapat",
                "description": "Kapak parçasını üst kısma yerleştirin ve 2 adet M4 cıvata ile emniyete alın.",
                "visible_parts": ["part_001", "part_002", "part_003"],
                "highlight_parts": ["part_003"],
                "camera_position": [0, -50, 120],
                "duration": 45
            }
        ]
