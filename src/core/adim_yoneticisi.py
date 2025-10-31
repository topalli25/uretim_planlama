"""
Montaj adimlarini yonetir
"""


class AdimYoneticisi:
    """Montaj adimlarini kontrol eder"""

    def __init__(self, montaj_verisi=None):
        self.montaj_verisi = montaj_verisi
        self.adimlar = []
        self.mevcut_adim_indeksi = 0

        if montaj_verisi:
            self.adimlari_yukle(montaj_verisi.get('adimlar', []))

    def adimlari_yukle(self, adimlar):
        """
        Adimlari yukle

        Adim formati:
        {
            "adim_numarasi": 1,
            "baslik": "Tabani yerlestir",
            "aciklama": "Taban parcasini is tezgahina sabitle",
            "gorunur_parcalar": ["parca_001"],
            "vurgulu_parcalar": ["parca_001"],
            "kamera_pozisyonu": [0, 0, 100],
            "sure": 30
        }
        """
        self.adimlar = adimlar
        self.mevcut_adim_indeksi = 0

    def mevcut_adimi_al(self):
        """Mevcut adimi dondur"""
        if 0 <= self.mevcut_adim_indeksi < len(self.adimlar):
            return self.adimlar[self.mevcut_adim_indeksi]
        return None

    def sonraki_adim(self):
        """Sonraki adima gec"""
        if self.mevcut_adim_indeksi < len(self.adimlar) - 1:
            self.mevcut_adim_indeksi += 1
            return True
        return False

    def onceki_adim(self):
        """Onceki adima gec"""
        if self.mevcut_adim_indeksi > 0:
            self.mevcut_adim_indeksi -= 1
            return True
        return False

    def adima_git(self, adim_numarasi):
        """Belirli bir adima git (1-based index)"""
        indeks = adim_numarasi - 1
        if 0 <= indeks < len(self.adimlar):
            self.mevcut_adim_indeksi = indeks
            return True
        return False

    def adim_sayisi_al(self):
        """Toplam adim sayisi"""
        return len(self.adimlar)

    def ilerleme_al(self):
        """Ilerleme yuzdesi (0-100)"""
        if len(self.adimlar) == 0:
            return 0
        return int((self.mevcut_adim_indeksi / len(self.adimlar)) * 100)

    def ilk_adim_mi(self):
        """Ilk adimda miyiz?"""
        return self.mevcut_adim_indeksi == 0

    def son_adim_mi(self):
        """Son adimda miyiz?"""
        return self.mevcut_adim_indeksi == len(self.adimlar) - 1

    def tum_adimlari_al(self):
        """Tum adimlari dondur"""
        return self.adimlar

    def ornek_adimlar_olustur(self):
        """Ornek adimlar olustur"""
        return [
            {
                "adim_numarasi": 1,
                "baslik": "Adim 1: Tabani Hazirla",
                "aciklama": "Taban parcasini alin ve is tezgahina yerlestirin.",
                "gorunur_parcalar": ["parca_001"],
                "vurgulu_parcalar": ["parca_001"],
                "kamera_pozisyonu": [0, 0, 100],
                "sure": 30
            },
            {
                "adim_numarasi": 2,
                "baslik": "Adim 2: Govdeyi Takin",
                "aciklama": "Govde parcasini taban uzerine yerlestirin ve 4 adet M6 civata ile sabitleyin.",
                "gorunur_parcalar": ["parca_001", "parca_002"],
                "vurgulu_parcalar": ["parca_002"],
                "kamera_pozisyonu": [50, 50, 100],
                "sure": 60
            },
            {
                "adim_numarasi": 3,
                "baslik": "Adim 3: Kapagi Kapat",
                "aciklama": "Kapak parcasini ust kisma yerlestirin ve 2 adet M4 civata ile emniyete alin.",
                "gorunur_parcalar": ["parca_001", "parca_002", "parca_003"],
                "vurgulu_parcalar": ["parca_003"],
                "kamera_pozisyonu": [0, -50, 120],
                "sure": 45
            }
        ]
