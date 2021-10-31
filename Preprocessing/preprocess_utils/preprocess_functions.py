#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import re
import string
import numpy as np


# In[ ]:


def preprocess_name(string_in):
    brand_name = np.nan
    if string_in is not None:
        name_lowercased = string_in.lower()
        brand_name = string_in.split()[0]
        # Gom "Microsoft Surface... " và "Surface..." => "Microsoft"
        if "surface" in name_lowercased:
            brand_name = "Microsoft"
        # "Vivobook... " => "Asus"
        if "vivobook" in name_lowercased:
            brand_name = "Asus"
        if "macbook" in name_lowercased:
            brand_name = "Apple"
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


def preprocess_ram_type(string_in):
    types_of_RAM = ["LPDDR3", "DDR3L", "DDR3", "LPDDR4X", "DDR4"]
    ram_new = np.nan
    if string_in is None or str(string_in) == "nan":
        return ram_new

    ram_upercased = string_in.upper()
    for type in types_of_RAM:
        if type in ram_upercased:
            ram_new = type
            break
    return ram_new


# In[ ]:


def preprocess_storage(string_in):
    common_drive_capacity = ["128GB", "256GB", "512GB", "1TB"]
    new_drive = np.nan
    if string_in is not None and str(string_in) != "nan":
        drive_tight_uppercased = string_in.replace(" ", "").upper()
        for capacity in common_drive_capacity:
            if capacity in drive_tight_uppercased:
                new_drive = capacity
                break
    return new_drive


# In[ ]:


def preprocess_os(string_in):
    if string_in is None or str(string_in) == "nan":
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


def preprocess_webcam(string_in):
    if string_in is None or str(string_in) == "nan":
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
        # Nếu có '720p' hoặc 'hd' -> 'HD'
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

        # Độ phân giải 2K
        if "2K" in string_in:
            return "2160 x 1440"

        # Độ phân giải 4K
        if "4K/UHD" in string_in:
            return "3840 x 2160"

        # Tìm các chuỗi số trong string_in
        numbers = re.findall(r'\d+', string_in)
        return f'{numbers[0]} x {numbers[1]}'


# In[ ]:


def preprocess_battery(string_in):
    if not string_in or str(string_in) == "nan":
        return np.nan

    string_in = string_in.lower()
    if 'wh' not in string_in:
        return np.nan

    string_in = string_in.replace(',', '')
    string_in = string_in.replace('(', '')
    string_in = string_in.replace(')', '')
    string_in = string_in.replace('whrs', 'wh')
    string_in = string_in.replace('whr', 'wh')
    string_in = string_in.replace('whs', 'wh')
    string_in = string_in.replace('-watt-hour lithium-polymer', 'wh')
    string_in = string_in.replace('wh integrated', 'wh')
    string_in = string_in.replace('wh li-ion', 'wh')
    string_in = string_in.replace(" wh", "wh")

    splits = string_in.split()
    for split in splits:
        if "wh" in split:
            return split.replace("wh", "")

    return string_in


def preprocessing_size_weight(string_in):
    if not string_in or str(string_in) == "nan":
        return [np.nan, np.nan, np.nan, np.nan]

    # Chuyển đơn vị g (gram) lên kg (kilogram)
    if "g" in string_in.split():
        g = float(string_in.split()[-2])
        kg = g / 1000
        string_in = string_in + str(kg)

    sizes = re.findall("\\d*\\.?,?\\d+", string_in)
    sizes = [x.replace(",", ".") for x in sizes]
    sizes = list(map(lambda x: float(x), sizes))
    sizes = sorted(sizes)[:4]
    sizes = sizes + [np.nan] * (4 - len(sizes))
    return sizes


def preprocess_thunderbolt(string_in):
    if not string_in or str(string_in) == "nan":
        return np.nan
    else:
        string_in = string_in.lower()
        # Kiểm tra trong chuỗi có 'thunderbolt' hay không
        if 'thunderbolt' in string_in:
            return 1  # Có -> trả về 1
        else:
            return 0  # Không -> trả về 0


def preprocess_antiglare(string_in):
    if not string_in or str(string_in) == "nan":
        return np.nan
    else:
        string_in = string_in.lower()
        # Kiểm tra trong chuỗi có 'chống chói' hay 'anti glare' không
        if 'chống chói' in string_in or 'anti glare' in string_in:
            return 1  # Có -> trả về 1
        else:
            return 0  # Không -> trả về 0


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
            # print(string_in)
            return np.nan


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
            elif 'quadro' in string_in:
                return "NVIDIA Quadro"
            else:
                print(string_in)
        # Kiểm tra Intel GPU
        elif ('intel' in string_in) or ('onboard' in string_in) or ('tích hợp' in string_in):
            return 'Intel'
        # Kiểm tra Microsoft GPU
        elif 'microsoft' in string_in:
            return 'Microsoft'
        else:
            # print(string_in)
            return np.nan


def preprocess_audio_tech(string_in):
    auto_tech_types = ["DTS", "Realtek", "Nahimic", "Dolby", "Harman", "Stereo", "TrueHarmony", "SonicMaster",
                       "Bang & Olufsen", "Smart AMP", "Waves MaxxAudio",
                       "HP Audio Boost"]

    if string_in is not None and str(string_in) != "nan":
        # Format nhiều cách thể hiện => 1 kiểu duy nhất
        string_in = string_in.replace("High Definition", "Realtek High Definition")
        string_in = string_in.replace("High-definition", "Realtek High Definition")

        for type in auto_tech_types:
            if type.lower() in string_in.lower():
                return type
        else:
            string_in = "Other"
    return string_in


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


def preprocess_ram_speed(string_in):
    if not string_in or str(string_in) == "nan":
        return np.nan

    string_in = string_in.lower()
    bus = re.match(r'\d+\ ?mhz', string_in)
    if bus:
        bus = int(bus.group().replace('mhz', ''))
    else:
        bus = np.nan
    return bus


def preprocess_wifi_tech(string_in):
    if string_in is None or str(string_in) == "nan":
        return np.nan
    else:
        string_in = string_in.lower().replace(" ", "")
        for punc in string.punctuation:
            string_in = string_in.replace(punc, "")
        # "ax" là chuẩn của Wi-Fi 6
        if "wifi6" in string_in or "ax" in string_in:
            string_in = "Wi-Fi 6"
        # "ac" là chuẩn của Wi-Fi 5
        elif "wifi5" in string_in or "ac" in string_in:
            string_in = "Wi-Fi 5"
        else:
            string_in = "Wi-Fi 5"
    return string_in


def preprocess_bluetooth_tech(string_in):
    if string_in is None or str(string_in) == "nan":
        return np.nan
    # Trích số thực
    string_in = re.findall("\\d*\\.?,?\\d+", string_in)
    string_in = sorted(string_in)
    if string_in:  # Trích thành công
        # Xử lí trường hợp chỉ trích được ra loại wifi
        if str(string_in[0]) == "802.11":
            string_in = np.nan
        else:
            string_in = string_in[0]
    return string_in


def preprocess_wireless(string_in):
    bluetooth = preprocess_bluetooth_tech(string_in)
    wifi = preprocess_wifi_tech(string_in)

    return bluetooth, wifi


def preprocess_lightning(string_in):
    # Kiểm tra giá trị trong ô trước khi bắt đầu xử lí
    if string_in is None or str(string_in) == "nan":
        return np.nan

    # Cột has_lightning chỉ có 3 giá trị: 'Có', 'Không có đèn' và nan

    # Có đèn thì return 1, không có đèn return 0
    if len(string_in) == 2:
        return 1
    else:
        return 0


def preprocess_new_warranty(string_in):
    # Kiểm tra giá trị trong ô trước khi bắt đầu xử lí
    if string_in is None or str(string_in) == "nan":
        return np.nan
    # Trả về số năm bảo hành, sau đó chuyển sang tháng
    return int(re.search('\d+', string_in).group()) * 12


def preprocess_material(string_in):
    # Kiểm tra giá trị trong ô trước khi bắt đầu xử lí
    if string_in is None or str(string_in) == "nan":
        return np.nan

    # Chia material thành 3 nhóm: Kim loại, hợp kim và nhựa

    string_in = string_in.lower()
    if ('nhôm' in string_in) or ('magie' in string_in) or ('hợp kim' in string_in):
        return 'Hợp kim'
    elif 'nhựa' in string_in:
        return 'Nhựa'
    else:
        return 'Kim loại'


# Xử lý Cpu_speed
def preprocess_cpu_speed(string_in):
    if string_in is None or str(string_in) == 'nan':  # None hoặc nan -> np.nan
        return np.nan

    output = re.findall("\\d*\\.?,?\\d+", string_in)  # trả về list chỉ chứa số
    output = [x.replace(",", ".") for x in output]  # thay dấu , = .
    output = list(map(lambda x: float(x), output))  # ép kiểu các số trong list -> float
    output = output[0]  # lấy phần tử đầu tiên của list vì list chỉ có 1 phần tử

    return output


# Xử lý Max_Cpu_Speed
def preprocess_max_cpu_speed(string_in):
    if string_in is None or str(string_in) == "nan":
        return np.nan
    output = re.findall("\\d*\\.?,?\\d+", string_in)
    output = [x.replace(",", ".") for x in output]
    output = list(map(lambda x: float(x), output))
    output = output[0]

    return output


# Xử lý Ram
def preprocess_ram(string_in):
    if string_in is None or str(string_in) == "nan":
        return np.nan
    output = re.findall("\\d*\\.?,?\\d+", string_in)  # trả về list
    output = [x.replace(",", ".") for x in output]
    output = list(map(lambda x: float(x), output))
    output = int(output[0])

    return output


# Xử lý Max_ram
def preprocess_max_ram(string_in):
    if string_in is None or str(string_in) == "nan":
        return np.nan
    output = re.findall("\\d*\\.?,?\\d+", string_in)  # trả về list
    output = [x.replace(",", ".") for x in output]
    output = list(map(lambda x: float(x), output))

    # Nếu không hổ trợ nâng cấp ram -> np.nan
    if output == []:
        return np.nan
    else:
        output = int(output[0])

    return output


def preprocess_new_price(string_in):
    if string_in is None or str(string_in) == "nan":
        return np.nan
    # Trích số thực
    output = re.findall("\\d*\\.?\\d+\\.?\d+", string_in)
    output = [x.replace(".", "") for x in output]
    output = list(map(lambda x: float(x), output))

    # Xử lí trường hợp chỉ có thông số bluetooth hoặc wifi
    if len(output) == 0:
        return np.nan
    else:
        return output[0]


def preprocess_used_warranty(string_in):
    if string_in is None or str(string_in) == "nan":
        return np.nan
    # Trích số thực
    output = re.findall("\\d*\\.?,?\\d+", string_in)
    output = [x.replace(",", ".") for x in output]
    # print(output)
    output = list(map(lambda x: float(x), output))

    # Xử lí trường hợp chỉ có thông số bluetooth hoặc wifi
    if len(output) == 0:
        return np.nan
    else:
        return output[0]
