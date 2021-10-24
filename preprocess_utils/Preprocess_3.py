# str0 = '4-cell Li-ion, 57 Whs' -> 57
# str1 = 'Khoảng 10 tiếng' -> nan
# str2 = '4-cell Li-ion, 57 Wh' -> 57
# str3 = '72 Wh Li-Ion' -> 72
# str4 = '4-Cell Battery, 52 Whr (Integrated)' -> 52
# str5 = '58.2-watt-hour lithium-polymer, 61W USB-C Power Adapter' -> nan
# str6 = '4Cell 60.7Wh' -> 60.7
# str7 = '3 Cell Int (56Wh)' -> 56
# str8 = '4 Cell 67WHr Lithium-Polymer' -> 67
# str9 = '4 cell 67 Wh' -> 67
# str10 = '57 Wh' -> 57
# str11 = 'Li-ion, 56 Wh' -> 56

import numpy as np

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

#%%
#df["Pin"] = df["Thông tin Pin"].apply(lambda s: thongTinPin(s))
#df["Pin"].value_counts()