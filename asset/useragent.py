import json
import random
import os
import hashlib
import base64
import string

def load_devices_from_json(file_path="asset/devices.json"):
    """
    Load devices from JSON file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('devices', [])
    except FileNotFoundError:
        print(f"File {file_path} tidak ditemukan!")
        return []
    except json.JSONDecodeError:
        print(f"File {file_path} format JSON tidak valid!")
        return []

def generate_mid(prefix="ae", length=22):
    """
    Generate MID dengan prefix tertentu
    Karakter yang diizinkan: huruf, angka, dan underscore (_)
    """
    chars = string.ascii_letters + string.digits + "_"
    random_part = ''.join(random.choices(chars, k=length - len(prefix)))
    return prefix + random_part

def generate_mid_from_device(prefix="ae", device_info=None):
    """
    Generate MID dari informasi device (lebih konsisten)
    Panjang total: 22 karakter (prefix 2 + 20 karakter)
    Karakter yang diizinkan: huruf, angka, dan underscore (_)
    """
    if device_info:
        device_str = f"{device_info.get('manufacturer', '')}{device_info.get('model', '')}{device_info.get('device_name', '')}"
        hash_obj = hashlib.md5(device_str.encode())
        hash_part = base64.b64encode(hash_obj.digest()).decode()
        hash_part = hash_part.replace('/', '_').replace('+', '0').replace('=', '')
        hash_part = hash_part[:20]
        return f"{prefix}{hash_part}"
    else:
        return generate_mid(prefix)

def generate_instagram_ua(
    version="436.0.0.41.73",
    android="32/12",
    dpi="220dpi",
    resolution="960x540",
    language="en_US",
    build="1006556565",
    random_device=True,
    custom_device=None,
    devices_file="asset/devices.json"
):
    """
    Generate Instagram User-Agent dengan load dari file
    Returns: dict {ua: user_agent, mid: mid, device: device_info}
    """
    
    # Load devices dari file
    DEVICES = load_devices_from_json(devices_file)
    
    if not DEVICES:
        print("Tidak ada device, pakai default")
        DEVICES = [
            {"manufacturer": "Xiaomi", "model": "M2101K7AG", "device_name": "Redmi Note 10", "brand": "Xiaomi"},
            {"manufacturer": "samsung", "model": "SM-A525F", "device_name": "Galaxy A52", "brand": "samsung"},
        ]
    
    # Pilih device
    if custom_device:
        manufacturer, model, device_name, brand = custom_device
        device_info = {
            "manufacturer": manufacturer,
            "model": model,
            "device_name": device_name,
            "brand": brand
        }
    elif random_device:
        device = random.choice(DEVICES)
        manufacturer = device['manufacturer']
        model = device['model']
        device_name = device['device_name']
        brand = device['brand']
        device_info = device
    else:
        # Default ke device pertama
        device = DEVICES[0]
        manufacturer = device['manufacturer']
        model = device['model']
        device_name = device['device_name']
        brand = device['brand']
        device_info = device
    
    # Build User-Agent
    user_agent = (
        f"Instagram {version} Android "
        f"({android}; {dpi}; {resolution}; "
        f"{manufacturer}; {model}; "
        f"{device_name}; {brand}; "
        f"{language}; {build})"
    )
    
    # Generate MID dari device info
    mid = generate_mid_from_device("ae", device_info)
    
    return {"ua": user_agent, "mid": mid, "device": device_info}

def generate_barcelona_ua(
    version="436.0.0.44.75",
    android="32/12",
    dpi="220dpi",
    resolution="960x540",
    language="en_US",
    build="1006783842",
    random_device=True,
    custom_device=None,
    devices_file="asset/devices.json"
):
    """
    Generate Barcelona User-Agent (mirip Instagram)
    Returns: dict {ua: user_agent, mid: mid, device: device_info}
    """
    
    # Load devices dari file
    DEVICES = load_devices_from_json(devices_file)
    
    if not DEVICES:
        print("Tidak ada device, pakai default")
        DEVICES = [
            {"manufacturer": "Xiaomi", "model": "M2101K7AG", "device_name": "Redmi Note 10", "brand": "Xiaomi"},
            {"manufacturer": "samsung", "model": "SM-A525F", "device_name": "Galaxy A52", "brand": "samsung"},
            {"manufacturer": "OPPO", "model": "CPH1912", "device_name": "OPPO CPH1912", "brand": "OPPO"},
        ]
    
    # Pilih device
    if custom_device:
        manufacturer, model, device_name, brand = custom_device
        device_info = {
            "manufacturer": manufacturer,
            "model": model,
            "device_name": device_name,
            "brand": brand
        }
    elif random_device:
        device = random.choice(DEVICES)
        manufacturer = device['manufacturer']
        model = device['model']
        device_name = device['device_name']
        brand = device['brand']
        device_info = device
    else:
        device = DEVICES[0]
        manufacturer = device['manufacturer']
        model = device['model']
        device_name = device['device_name']
        brand = device['brand']
        device_info = device
    
    # Build User-Agent Barcelona
    user_agent = (
        f"Barcelona {version} Android "
        f"({android}; {dpi}; {resolution}; "
        f"{manufacturer}; {model}; "
        f"{device_name}; {brand}; "
        f"{language}; {build})"
    )
    
    # Generate MID dari device info
    mid = generate_mid_from_device("ak", device_info)
    
    return {"ua": user_agent, "mid": mid, "device": device_info}
