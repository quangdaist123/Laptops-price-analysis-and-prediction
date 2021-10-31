# Reload module
import sys
if sys.modules.get("Preprocessing.preprocess_utils.preprocess_functions"):
    del sys.modules["Preprocessing.preprocess_utils.preprocess_functions"]

import Preprocessing.preprocess_utils.preprocess_functions as pf

# In[ ]:


import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

alternative_names = \
    {'Bảo hành cũ': 'used_warranty',
     'Giá máy cũ': 'used_price',
     'Tên': 'name',
     'Giá máy mới': "new_price",
     'Bảo hành mới': "new_warranty",
     'Tiết kiệm': "savings",
     'Công nghệ CPU': 'cpu_tech',
     'Số nhân': 'num_core',
     'Số luồng': 'num_thread',
     'Tốc độ CPU': "cpu_speed",
     'Tốc độ tối đa': "max_cpu_speed",
     'Bộ nhớ đệm': "cached_cpu",
     'RAM': 'ram',
     'Loại RAM': 'ram_type',
     'Tốc độ Bus RAM': 'ram_speed',
     'Hỗ trợ RAM tối đa': 'max_ram',
     'Ổ cứng': 'storage',
     'Màn hình': 'screen',
     'Độ phân giải': 'resolution',
     'Tần số quét': "scan_frequency",
     'Công nghệ màn hình': 'screen_tech',
     'Màn hình cảm ứng': 'has_touch_screen',
     'Card màn hình': 'graphics',
     'Công nghệ âm thanh': 'audio_tech',
     'Cổng giao tiếp': 'ports',
     'Kết nối không dây': 'wireless',
     'Khe đọc thẻ nhớ': 'sd_slot',
     'Webcam': 'webcam',
     'Tính năng khác': 'others',
     'Đèn bàn phím': 'has_lightning',
     'Kích thước, trọng lượng': 'size_weight',
     'Chất liệu': 'material',
     'Thông tin Pin': 'battery',
     'Hệ điều hành': 'os',
     'Thời điểm ra mắt': 'released'
     }

# In[ ]:

df = pd.read_csv("Dataset/Raw/raw_data_TGDD_used_renamed.csv")
df_take_first_occurence = df.groupby("name", as_index=False).first()
df = df_take_first_occurence

# %%


df["name"] = df["name"].apply(lambda s: pf.preprocess_name(s))
df["used_price"] = df["used_price"].apply(lambda s: pf.preprocess_new_price(s))
df["new_price"] = df["new_price"].apply(lambda s: pf.preprocess_new_price(s))

df['cpu_tech'] = df['cpu_tech'].apply(lambda s: pf.preprocess_cpu(s))
df["ram_type"] = df["ram_type"].apply(lambda s: pf.preprocess_ram_type(s))
df["ram_speed"] = df["ram_speed"].apply(lambda s: pf.preprocess_ram_speed(s))
df["storage"] = df["storage"].apply(lambda s: pf.preprocess_storage(s))
df["audio_tech"] = df["audio_tech"].apply(lambda s: pf.preprocess_audio_tech(s))
df["resolution"] = df["resolution"].apply(lambda s: pf.preprocess_resolution(s))
df["os"] = df["os"].apply(lambda s: pf.preprocess_os(s))
df['graphics'] = df['graphics'].apply(lambda s: pf.preprocess_gpu(s))
df['cpu_speed'] = df['cpu_speed'].apply(lambda s: pf.preprocess_cpu_speed(s))
df['max_cpu_speed'] = df['max_cpu_speed'].apply(lambda s: pf.preprocess_max_cpu_speed(s))
df['ram'] = df['ram'].apply(lambda s: pf.preprocess_ram(s))
df['max_ram'] = df['max_ram'].apply(lambda s: pf.preprocess_max_ram(s))
df['has_lightning'] = df['has_lightning'].apply(lambda s: pf.preprocess_lightning(s))
df['material'] = df['material'].apply(lambda s: pf.preprocess_material(s))
df['new_warranty'] = df['new_warranty'].apply(lambda s: pf.preprocess_new_warranty(s))
df["used_warranty"] = df["used_warranty"].apply(lambda s: pf.preprocess_used_warranty(s))
df["bluetooth_tech"] = df["wireless"].apply(lambda s: pf.preprocess_wireless(s)[0])
df["wifi_tech"] = df["wireless"].apply(lambda s: pf.preprocess_wireless(s)[1])
df["webcam"] = df["webcam"].apply(lambda s: pf.preprocess_webcam(s))
df["battery"] = df["battery"].apply(lambda s: pf.preprocess_battery(s))
df["weight"] = df["size_weight"].apply(lambda s: pf.preprocessing_size_weight(s)[0])
df["thickness"] = df["size_weight"].apply(lambda s: pf.preprocessing_size_weight(s)[1])
df["width"] = df["size_weight"].apply(lambda s: pf.preprocessing_size_weight(s)[2])
df["length"] = df["size_weight"].apply(lambda s: pf.preprocessing_size_weight(s)[3])
df['has_thundebolt'] = df['ports'].apply(lambda s: pf.preprocess_thunderbolt(s))
df['has_antiglare'] = df['screen_tech'].apply(lambda s: pf.preprocess_antiglare(s))

# %%
df.to_csv("tidydataset.csv", index=False)
