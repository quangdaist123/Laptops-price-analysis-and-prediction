#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import f_oneway
from math import ceil


# In[ ]:


def preprocess_name(name):
    filters = ["laptop", "laptop gaming"]
    brand_name = np.nan
    if name is not None:
        name_lowercased = name.lower()
        # Bỏ chữ "Laptop" và "Laptop gaming"
        for filter in filters:
            if name_lowercased[:len(filter)] == filter:
                removed_laptop_word = name[len(filter):]
                brand_name = removed_laptop_word.split()[0]
        # Gom "Microsoft Surface... " và "Surface..." => "Microsoft"
        if "surface" in name_lowercased:
            brand_name = "Microsoft"
        # "Vivobook... " => "Asus"
        if "vivobook" in name_lowercased:
            brand_name = "Asus"
        # Trừ "HP", "MSI", "LG", Chỉ có chữ đầu tiên của các tên hãng đều được in hoa
        if str(brand_name) != "nan" and brand_name not in ["HP", "MSI", "LG"]:
            brand_name = brand_name.capitalize()

    return brand_name


# In[ ]:


def filter_non_laptops(df):
    df = df.copy()
    freq = dict(df["brand"].value_counts())
    new_column = []
    for i, row in df.iterrows():
        if str(row["brand"]) != "nan" and freq[row["brand"]] == 1:
            new_column.append(np.nan)
        else:
            new_column.append(row["brand"])
    df["brand"] = new_column
    df.dropna(subset=['brand'], inplace=True)
    return df


# In[ ]:


def preprocess_RAM(ram):
    types_of_RAM = ["LPDDR4X", "DDR4"]
    ram_new = np.nan
    if ram is not None and str(ram) != "nan":
        ram_upercased = ram.upper()
        for type in types_of_RAM:
            if type in ram_upercased:
                ram_new = type
                break
    return ram_new


# In[ ]:


def preprocess_drive(drive):
    common_drive_capacity = ["128GB", "256GB", "512GB", "1TB"]
    new_drive = np.nan
    if drive is not None and str(drive) != "nan":
        drive_tight_uppercased = drive.replace(" ", "").upper()
        for capacity in common_drive_capacity:
            if capacity in drive_tight_uppercased:
                new_drive = capacity
                break
    return new_drive


# In[ ]:


def preprocess_os(string_in):
    if str(string_in) == 'nan' or string_in == None or type(string_in) == np.float:
        return np.nan
    else:
        string_in = string_in.lower()
        
        # Nếu có 'mac' -> MacOS
        if 'mac' in string_in:
            return 'MacOS'
        # Nếu có 'win' -> Windows
        elif 'win' in string_in:
            return 'Windows'
        # FreeDOS -> np.nan
        else:
            return np.nan


# In[ ]:


def preprocess_camera(string_in):
    if str(string_in) == 'nan' or string_in == None:
        return np.nan
    else:
        string_in = string_in.lower().replace(',', '')
        substrings = string_in.split()
        
        # Nếu có 'vga' hoặc chỉ có 'webcam' -> 'VGA' 
        if 'vga' in substrings or len(substrings) == 1:
            return 'VGA'
        # Nếu có 'fhd' -> 'FHD'
        elif 'fhd' in substrings:
            return 'FHD'
        else:
            # Nếu có cả 'ir' và ('720p' hoặc 'hd') -> 'HD IR'
            if 'ir' in substrings and ('hd' in substrings or '720p' in substrings):
                return 'HD IR'
            # Nếu chỉ có 'ir' -> 'IR'
            elif 'ir' in substrings:
                return 'IR'
            # Nếu chỉ có '720p' hoặc 'hd' -> 'HD'
            elif 'hd' in substrings or '720p' in substrings:
                return 'HD'
            # Các trường hợp còn lại -> np.nan
            else:
                return np.nan


# In[ ]:


def preprocess_resolution(string_in):
    if str(string_in) == 'nan' or string_in == None:
        return np.nan
    else:
        # Tìm các chuỗi số trong string_in
        numbers = re.findall(r'\d+', string_in)
        return f'{numbers[0]} x {numbers[1]}'   


# In[ ]:


def preprocess_battery(_str):
    if not _str or str(_str) == "nan":
        return np.nan
  
    _str = _str.lower()
    if 'wh' not in _str:
        return np.nan

    _str = _str.replace(',', '')
    _str = _str.replace('(','')
    _str = _str.replace(')','')
    _str = _str.replace('whrs','wh')
    _str = _str.replace('whr','wh')
    _str = _str.replace('whs','wh')
    _str = _str.replace('-watt-hour lithium-polymer','wh')
    _str = _str.replace('wh integrated','wh')
    _str = _str.replace('wh li-ion','wh')
    _str = _str.replace(" wh", "wh")

    splits = _str.split()
    for split in splits:
        if "wh" in split:
            return split.replace("wh", "")

    return _str


def preprocessing_size(_str):
    if not _str or str(_str) == "nan":
        return np.nan, np.nan, np.nan

    sizes = re.findall("\\d*\\.?,?\\d+", _str)
    sizes = list(map(lambda x: float(x.replace(",", ".")), sizes))
    if 'mm' in _str:
        # Xử lí trường hợp ghi nhầm "cm" thành "mm" trong "29.21 x 20.142 x 0.85 mm"
        # Không có laptop nào có kích thước < 50mm (5cm)
        if all(x < 50 for x in sizes):
            sizes = sizes
        else:
            # Chuyển từ mm sang cm
            sizes = [round(float(x) / 10, 1) for x in sizes]
    # Xử lí trường hợp có nhiều số trong list
    # print(sizes)
    sizes = sorted(sizes, reverse=True)[:3]
    return sizes

def preprocess_thunderbolt(string_in):
    if not string_in or str(string_in) == "nan":
        return np.nan
    else:
        string_in = string_in.lower()
        # Kiểm tra trong chuỗi có 'thunderbolt' hay không
        if 'thunderbolt' in string_in:
            return 1      # Có -> trả về 1
        else:
            return 0      # Không -> trả về 0
        
def preprocess_AntiGlare(string_in):
    if not string_in or str(string_in) == "nan":
        return np.nan
    else:
        string_in = string_in.lower()
        # Kiểm tra trong chuỗi có 'chống chói' hay 'anti glare' không
        if 'chống chói' in string_in or 'anti glare' in string_in:
            return 1      # Có -> trả về 1
        else:
            return 0      # Không -> trả về 0
        
def preprocess_cpu(string_in):
    if not string_in or str(string_in) == "nan":
        return np.nan
    else:
        string_in = string_in.lower()
        # Kiểm tra Apple
        if 'apple' in string_in or 'm1' in string_in:
            return 'M1'   
        # Kiểm tra Intel Core i7
        elif 'i7' in string_in:
            return 'i7' 
        # Kiểm tra Intel Core i5
        elif 'i5' in string_in:
            return 'i5'
        # Kiểm tra Intel Core i3
        elif 'i3' in string_in:
            return 'i3'
        elif 'pentium' in string_in:
            return 'pentium'
        # Kiểm tra AMD Ryzen 3
        elif 'ryzen 3' in string_in:
            return 'R3'
        # Kiểm tra AMD Ryzen 5
        elif 'ryzen 5' in string_in:
            return 'R5'
        # Kiểm tra AMD Ryzen 7
        elif 'ryzen 7' in string_in:
            return 'R7'
        # Kiểm tra AMD Ryzen 9
        elif 'ryzen 9' in string_in:
            return 'R9'
        elif 'microsoft' in string_in:
            return 'Microsoft'
        else:
            print(string_in)
            
def preprocess_gpu(string_in):
    if not string_in or str(string_in) == "nan":
        return np.nan
    else:
        string_in = string_in.lower()
        # Kiểm tra Apple GPU
        if 'apple' in string_in or 'm1' in string_in:
            return 'Apple'   
        # Kiểm tra AMD GPU
        elif 'amd' in string_in:
            return 'AMD' 
        # Kiểm tra NVIDIA GPU
        elif ('nvidia' in string_in) or ('geforce' in string_in):
            if 'rtx' in string_in:
                return 'NVIDIA RTX'
            elif 'gtx' in string_in:
                return 'NVIDIA GTX'
            elif 'mx' in string_in:
                return 'NVIDIA MX'
            else:
                print(string_in)
        # Kiểm tra Intel GPU
        elif ('intel' in string_in) or ('onboard' in string_in) or ('tích hợp' in string_in):
            return 'Intel'
        # Kiểm tra Microsoft GPU
        elif 'microsoft' in string_in:
            return 'Microsoft'
        else:
            print(string_in)
            
def preprocess_audio_tech(raw_input):
    auto_tech_types = ["DTS", "Realtek", "Nahimic", "Dolby", "Harman", "Stereo"]
    # new_input = np.nan

    if raw_input is not None and str(raw_input) != "nan":
        raw_input = raw_input.replace("High Definition", "Realtek High Definition")
        raw_input = raw_input.replace("High-definition", "Realtek High Definition")
        for type in auto_tech_types:
            if type.lower() in raw_input.lower():
                return type
        else:
            raw_input = "Other"
    return raw_input


def preprocess_RAM_tiki(string_in):
    if not string_in['RAM'] or str(string_in['RAM']) == "nan":
        return np.nan, np.nan, np.nan
    else:
        # Lấy dung lượng RAM
        string_in['RAM'] = string_in['RAM'].strip()
        
        if string_in['RAM'][:2].isdigit():
            ram_capacity = string_in['RAM'][:2]
        else:
            ram_capacity = string_in['RAM'][0]
    
        # Lấy loại RAM
        types_of_RAM = ["LPDDR4X", "DDR4"]
        ram_type = np.nan
        for type in types_of_RAM:
            if type in string_in['RAM']:
                ram_type = type
                break
        
        # Lấy bus RAM
        string_in['RAM'] = string_in['RAM'].lower()
        bus = re.match(r'\d+\ ?mhz', string_in['RAM'])
        if bus:
            bus = int(bus.replace('mhz', ''))
        else:
            bus = np.nan
        # đk
        if (str(string_in['Loại RAM']) != 'nan') and (str(ram_type) == 'nan'):
            ram_type = string_in['Loại RAM']
            
        if str(string_in['Tốc độ Bus RAM']) != 'nan' and str(bus) == 'nan':
            bus = string_in['Tốc độ Bus RAM']
        
    return (ram_capacity, ram_type, bus)