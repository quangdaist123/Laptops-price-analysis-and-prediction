# str0 = 'Dài 313.4 mm - Rộng 215.2 mm - Dày 16.8 mm' -> ['3134', '2152', '168']
# str1 = '\n355.9 x 243.4 x 16.8 mm\n14.01 x 9.58 x 0.66"\n' -> ['3559', '2434', '168']
# str2 = 'Dài Dài 324 mm - - Rộng Rộng 213 mm - Dày Dày 15.9 mm' -> ['3240', '2130', '159']
# str3 = '30.5 x 21.1 x 1.19 ~ 1.39 (cm)' -> ['3050', '2110', '119']
# str4 = 'Front height 18.99 mmWidth 358.5 mmDepth 235.56 mm' -> ['1899', '3585', '235']
# str5 = '1.89 x 35.61 x 23.45 cm (H x W x D)' -> ['1890', '3561', '234']
# str6 = '356.8 x 233.7 x 16.9 mm' -> ['3568', '2337', '169']
# str7 = '\n\n\nKích thước & Trọng lượng\n1. Chiều cao: 13,9 - 15,9 mm (0,55 "- 0,625") | 2. Chiều rộng: 296,
# 78 mm (11,68 ") | 3. Chiều sâu: 210 mm (8,27") | Trọng lượng khởi điểm: 1,25 kg (2,75 lb)\n\n\n' -> ['1000',
# '1390', '159']
# str8 = 'Ngang 30.41 x Dày 1.56 x Sâu 21.24 cm' -> ['3041', '1560', '212']
# str9 = '(Dài x Rộng x Dày) 308.1 x 223.27 x 14.48 mm' -> ['3081', '2232', '144']
# str10 = '1.49 x 30.41 x 21.24 cm' -> ['1490', '3041', '212']

# Mục đích của tui là đưa 1 chuỗi str -> Get 3 số đầu tiên -> chuyển về dạng Dài (4 chữ số ) x rộng (4 chữ số) x dày
# (3 chữ số)
import numpy as np
import pandas as pd
import re

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)



# %%

def kichThuoc(_str):
    if not _str or str(_str) == "nan":
        return np.nan

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
hi = "Front height 18.99 mmWidth 358.5 mmDepth 235.56 mm"
re.findall("[+-]?\\d*\\.?,?\\d+", hi)

# %%
for i, row in df.iterrows():
    # if str(row["Kích thước"]) != "nan" and len(kichThuoc(row["Kích thước"])) > 4:
    if str(row["Kích thước"]) != "nan" and (kichThuoc(row["Kích thước"])) == [2.9, 2.0, 0.1]:
        print(i, row["Kích thước"])
        print(i, kichThuoc(row["Kích thước"]))
