"""
Yardımcı fonksiyonlar ve araçlar
"""
import json
import os
from pathlib import Path


def load_json(file_path):
    """JSON dosyasını yükle"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data, file_path):
    """JSON dosyasına kaydet"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_project_root():
    """Proje kök dizinini döndür"""
    return Path(__file__).parent.parent.parent


def get_config():
    """Config dosyasını yükle"""
    config_path = get_project_root() / 'config.json'
    return load_json(config_path)


def ensure_dir(directory):
    """Dizin yoksa oluştur"""
    os.makedirs(directory, exist_ok=True)
