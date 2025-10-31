"""
Yardimci fonksiyonlar ve araclar
"""
import json
import os
from pathlib import Path


def json_yukle(dosya_yolu):
    """JSON dosyasini yukle"""
    with open(dosya_yolu, 'r', encoding='utf-8') as f:
        return json.load(f)


def json_kaydet(veri, dosya_yolu):
    """JSON dosyasina kaydet"""
    with open(dosya_yolu, 'w', encoding='utf-8') as f:
        json.dump(veri, f, indent=2, ensure_ascii=False)


def proje_kok_dizini_al():
    """Proje kok dizinini dondur"""
    return Path(__file__).parent.parent.parent


def konfig_al():
    """Config dosyasini yukle"""
    konfig_yolu = proje_kok_dizini_al() / 'config.json'
    return json_yukle(konfig_yolu)


def dizin_olustur(dizin):
    """Dizin yoksa olustur"""
    os.makedirs(dizin, exist_ok=True)
