"""
Montaj ve alt montaj yonetimi
"""
from pathlib import Path
from src.utils.yardimcilar import json_yukle, json_kaydet


class MontajYoneticisi:
    """Montaj bilgilerini yonetir"""

    def __init__(self, montaj_dizini='data/assemblies'):
        self.montaj_dizini = Path(montaj_dizini)
        self.mevcut_montaj = None
        self.parcalar = {}

    def montaj_yukle(self, montaj_dosyasi):
        """
        Montaj JSON dosyasini yukle

        Montaj JSON formati:
        {
            "isim": "Ana Montaj",
            "aciklama": "Urun montaji",
            "parcalar": [
                {
                    "id": "parca_001",
                    "isim": "Govde",
                    "model_dosyasi": "govde.step",
                    "renk": [1.0, 0.0, 0.0],
                    "gorunur": true
                }
            ],
            "adimlar": [...] # adim_yoneticisi tarafindan yonetilir
        }
        """
        montaj_yolu = self.montaj_dizini / montaj_dosyasi
        self.mevcut_montaj = json_yukle(montaj_yolu)

        # Parcalari indexle
        self.parcalar = {parca['id']: parca for parca in self.mevcut_montaj.get('parcalar', [])}

        return self.mevcut_montaj

    def parca_al(self, parca_id):
        """Belirli bir parcayi getir"""
        return self.parcalar.get(parca_id)

    def tum_parcalari_al(self):
        """Tum parcalari getir"""
        return self.mevcut_montaj.get('parcalar', [])

    def gorunur_parcalari_al(self):
        """Gorunur parcalari getir"""
        return [parca for parca in self.tum_parcalari_al() if parca.get('gorunur', True)]

    def parca_gorunurlugunu_ayarla(self, parca_id, gorunur):
        """Parca gorunurlugunu ayarla"""
        if parca_id in self.parcalar:
            self.parcalar[parca_id]['gorunur'] = gorunur
            # Ana montajda da guncelle
            for parca in self.mevcut_montaj['parcalar']:
                if parca['id'] == parca_id:
                    parca['gorunur'] = gorunur
                    break

    def montaj_bilgisi_al(self):
        """Montaj bilgilerini dondur"""
        if not self.mevcut_montaj:
            return None

        return {
            'isim': self.mevcut_montaj.get('isim', 'Isimsiz'),
            'aciklama': self.mevcut_montaj.get('aciklama', ''),
            'toplam_parca': len(self.tum_parcalari_al()),
            'gorunur_parca': len(self.gorunur_parcalari_al())
        }

    def ornek_montaj_olustur(self, cikti_dosyasi='ornek_montaj.json'):
        """Ornek montaj dosyasi olustur"""
        ornek = {
            "isim": "Ornek Montaj",
            "aciklama": "Test amacli ornek montaj projesi",
            "parcalar": [
                {
                    "id": "parca_001",
                    "isim": "Taban",
                    "model_dosyasi": "taban.step",
                    "renk": [0.8, 0.8, 0.8],
                    "gorunur": True
                },
                {
                    "id": "parca_002",
                    "isim": "Govde",
                    "model_dosyasi": "govde.step",
                    "renk": [0.2, 0.6, 1.0],
                    "gorunur": True
                },
                {
                    "id": "parca_003",
                    "isim": "Kapak",
                    "model_dosyasi": "kapak.step",
                    "renk": [1.0, 0.2, 0.2],
                    "gorunur": True
                }
            ],
            "adimlar": []
        }

        cikti_yolu = self.montaj_dizini / cikti_dosyasi
        json_kaydet(ornek, cikti_yolu)
        return cikti_yolu
