# str0 = 'Dài 313.4 mm - Rộng 215.2 mm - Dày 16.8 mm' -> ['3134', '2152', '168']
# str1 = '\n355.9 x 243.4 x 16.8 mm\n14.01 x 9.58 x 0.66"\n' -> ['3559', '2434', '168']
# str2 = 'Dài Dài 324 mm - - Rộng Rộng 213 mm - Dày Dày 15.9 mm' -> ['3240', '2130', '159']
# str3 = '30.5 x 21.1 x 1.19 ~ 1.39 (cm)' -> ['3050', '2110', '119']
# str4 = 'Front height 18.99 mmWidth 358.5 mmDepth 235.56 mm' -> ['1899', '3585', '235']
# str5 = '1.89 x 35.61 x 23.45 cm (H x W x D)' -> ['1890', '3561', '234']
# str6 = '356.8 x 233.7 x 16.9 mm' -> ['3568', '2337', '169']
# str7 = '\n\n\nKích thước & Trọng lượng\n1. Chiều cao: 13,9 - 15,9 mm (0,55 "- 0,625") | 2. Chiều rộng: 296,78 mm (11,68 ") | 3. Chiều sâu: 210 mm (8,27") | Trọng lượng khởi điểm: 1,25 kg (2,75 lb)\n\n\n' -> ['1000', '1390', '159']
# str8 = 'Ngang 30.41 x Dày 1.56 x Sâu 21.24 cm' -> ['3041', '1560', '212']
# str9 = '(Dài x Rộng x Dày) 308.1 x 223.27 x 14.48 mm' -> ['3081', '2232', '144']
# str10 = '1.49 x 30.41 x 21.24 cm' -> ['1490', '3041', '212']

#Mục đích của tui là đưa 1 chuỗi str -> Get 3 số đầu tiên -> chuyển về dạng Dài (4 chữ số ) x rộng (4 chữ số) x dày (3 chữ số)
import numpy as np
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

import re

def kichThuoc(_str):
  if not _str:
    return np.nan
  
  _str = _str.replace(',','') #2 dòng này lúc tui làm thì tui nhớ tác dụng, giờ tui cũng không rõ nữa @@
  _str = _str.replace('.','') #
  #Vì kích thước có 2 đơn vị là mm và cm nên tui sẽ xét 2 trường hợp 'mm' và 'cm'
  #ý tưởng của tui sẽ đồng bộ về số có 4 chữ số, xét tương quan thì nó sẽ không có ảnh hưởng nhiều, cũng có thể dễ dàng chuyển về đơn vị mình muốn
  if 'mm' in _str:
    _str = re.findall(r'\d+', _str)
    _str_ = []
    for i in _str:
      i = i + '0000'#thực ra thì cộng thêm bao nhiều chữ số cũng được, mục đích để các số phải có số chữ số >= 4
      i = i[0:4]#lấy 4 chữ số đầu tiên 
      _str_.append(i)
    x = _str_[2] #Dày nằm ở vị trí số 3
    _str_[2] = x[0:3] #Vì chiều dày chỉ có 3 chữ số nên chỉ lấy ngang 3 chữ số
    return _str_[0:3]#vì có những dòng sẽ có nhiều hơn 3 phần tử, mà mình chỉ cần lấy dài x rộng x dày, mà theo tui thấy thì nó chỉ nằm ở 3 phần tử đầu nên tui sẽ lấy 3 phần tử đầu
  elif 'cm' in _str:
    _str = re.findall(r'\d+', _str)
    _str_ = []
    for i in _str:
      i = i + '0000'
      i = i[0:4]#lấy 4 chữ số đầu tiên 
      _str_.append(i)
    x = _str_[2]
    _str_[2] = x[0:3]
    return _str_[0:3]
  else:
    return np.nan
