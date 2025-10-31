"""
Montaj adımlarını yönetir
"""


class AdimYoneticisi:
    """Montaj adımlarını kontrol eder"""

    def __init__(self, montaj_verisi=None):
        self.montaj_verisi = montaj_verisi
        self.adimlar = []
        self.mevcut_adim_indeksi = 0

        if montaj_verisi:
            self.adimlari_yukle(montaj_verisi.get('adimlar', []))

    def adimlari_yukle(self, adimlar):
        """
        Adımları yükle

        Adım formatı:
        {
            "adim_numarasi": 1,
            "baslik": "Tabanı yerleştir",
            "aciklama": "Taban parçasını iş tezgahına sabitle",
            "gorunur_parcalar": ["parca_001"],
            "vurgulu_parcalar": ["parca_001"],
            "kamera_pozisyonu": [0, 0, 100],
            "sure": 30
        }
        """
        self.adimlar = adimlar
        self.mevcut_adim_indeksi = 0

    def mevcut_adimi_al(self):
        """Mevcut adımı döndür"""
        if 0 <= self.mevcut_adim_indeksi < len(self.adimlar):
            return self.adimlar[self.mevcut_adim_indeksi]
        return None

    def sonraki_adim(self):
        """Sonraki adıma geç"""
        if self.mevcut_adim_indeksi < len(self.adimlar) - 1:
            self.mevcut_adim_indeksi += 1
            return True
        return False

    def onceki_adim(self):
        """Önceki adıma geç"""
        if self.mevcut_adim_indeksi > 0:
            self.mevcut_adim_indeksi -= 1
            return True
        return False

    def adima_git(self, adim_numarasi):
        """Belirli bir adıma git (1-based index)"""
        indeks = adim_numarasi - 1
        if 0 <= indeks < len(self.adimlar):
            self.mevcut_adim_indeksi = indeks
            return True
        return False

    def adim_sayisi_al(self):
        """Toplam adım sayısı"""
        return len(self.adimlar)

    def ilerleme_al(self):
        """İlerleme yüzdesi (0-100)"""
        if len(self.adimlar) == 0:
            return 0
        return int((self.mevcut_adim_indeksi / len(self.adimlar)) * 100)

    def ilk_adim_mi(self):
        """İlk adımda mıyız?"""
        return self.mevcut_adim_indeksi == 0

    def son_adim_mi(self):
        """Son adımda mıyız?"""
        return self.mevcut_adim_indeksi == len(self.adimlar) - 1

    def tum_adimlari_al(self):
        """Tüm adımları döndür"""
        return self.adimlar

    def ornek_adimlar_olustur(self):
        """Örnek adımlar oluştur"""
        return [
            {
                "adim_numarasi": 1,
                "baslik": "Adım 1: Tabanı Hazırla",
                "aciklama": "Taban parçasını alın ve iş tezgahına yerleştirin.",
                "gorunur_parcalar": ["parca_001"],
                "vurgulu_parcalar": ["parca_001"],
                "kamera_pozisyonu": [0, 0, 100],
                "sure": 30
            },
            {
                "adim_numarasi": 2,
                "baslik": "Adım 2: Gövdeyi Takın",
                "aciklama": "Gövde parçasını taban üzerine yerleştirin ve 4 adet M6 cıvata ile sabitleyin.",
                "gorunur_parcalar": ["parca_001", "parca_002"],
                "vurgulu_parcalar": ["parca_002"],
                "kamera_pozisyonu": [50, 50, 100],
                "sure": 60
            },
            {
                "adim_numarasi": 3,
                "baslik": "Adım 3: Kapağı Kapat",
                "aciklama": "Kapak parçasını üst kısma yerleştirin ve 2 adet M4 cıvata ile emniyete alın.",
                "gorunur_parcalar": ["parca_001", "parca_002", "parca_003"],
                "vurgulu_parcalar": ["parca_003"],
                "kamera_pozisyonu": [0, -50, 120],
                "sure": 45
            }
        ]
