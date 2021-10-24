#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np


# In[2]:


def preprocess_os(string_in):
    if not string_in:
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
    if not string_in:
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
    if not string_in:
        return np.nan
    else:
        import re
        # Tìm các chuỗi số trong string_in
        numbers = re.findall(r'\d+', string_in)
        return f'{numbers[0]} x {numbers[1]}'    

