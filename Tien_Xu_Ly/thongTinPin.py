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

def thongTinPin(_str):
  if not _str:
    return np.nan
  
  _bien = np.nan
  _str = _str.lower()
  if 'wh' not in _str:
      return np.nan
  
  _str = _str.replace('(','')
  _str = _str.replace(')','')
  _str = _str.replace('whs','wh')
  _str = _str.replace('whr','wh')
  _str = _str.replace('whrs','wh')
  _str = _str.replace('-watt-hour lithium-polymer','wh')
  _str = _str.replace('wh integrated','wh')
  _str = _str.replace('wh li-ion','wh')
  
  if ',' not in _str:
    _str = _str.replace("wh"," wh")
    chuoi_str = _str.split()
    for i in chuoi_str:
      if 'wh' in i:
        return _ketqua
      _ketqua = i
  
  elif ',' in _str:
    chuoi_str = _str.split(',')
    for i in chuoi_str:
      if 'wh' in i:
        _bien = i.replace(' ','')
        
  return _bien.replace('wh','')
