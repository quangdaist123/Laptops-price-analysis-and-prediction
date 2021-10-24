# Mục đích:
import numpy as np
import pandas as pd
import re

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

# %%
df = pd.read_csv("Raw/raw_combined_csv_ver2.csv")


# %%

def kichThuoc(_str):
    if not _str or str(_str) == "nan":
        return [np.nan, np.nan, np.nan]

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


# %%

df["size"] = df["Kích thước"].apply(lambda s: str(kichThuoc(s)))
df["size"].value_counts()

# %%
for i, row in df.iterrows():
    if str(row["Kích thước"]) != "nan" and (kichThuoc(row["Kích thước"])) == [2.9, 2.0, 0.1]:
        print(i, row["Kích thước"])
        print(i, kichThuoc(row["Kích thước"]))


# %%

# str0 = '4-cell Li-ion, 57 Whs' -> 57
# str1 = 'Khoảng 10 tiếng' -> nan
# str2 = '4-cell Li-ion, 57 Wh' -> 57
# str3 = '72 Wh Li-Ion' -> 72
# str4 = '4-Cell Battery, 52 Whr (Integrated)' -> 52
# str5 = '58.2-watt-hour lithium-polymer, 61W USB-C Power Adapter' -> nan

def thongTinPin(_str):
    if not _str or str(_str) == "nan":
        return np.nan

    _str = _str.lower()
    if 'wh' not in _str:
        return np.nan

    _str = _str.replace(',', '')
    _str = _str.replace('(', '')
    _str = _str.replace(')', '')
    _str = _str.replace('whrs', 'wh')
    _str = _str.replace('whr', 'wh')
    _str = _str.replace('whs', 'wh')
    _str = _str.replace('-watt-hour lithium-polymer', 'wh')
    _str = _str.replace('wh integrated', 'wh')
    _str = _str.replace('wh li-ion', 'wh')
    _str = _str.replace(" wh", "wh")

    splits = _str.split()
    for split in splits:
        if "wh" in split:
            return split.replace("wh", "")

    return _str


# %%
df["Pin"] = df["Thông tin Pin"].apply(lambda s: thongTinPin(s))
df["Pin"].value_counts()
