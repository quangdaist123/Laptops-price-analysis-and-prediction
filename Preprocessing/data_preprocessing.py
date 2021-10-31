# Reload module
import sys

if sys.modules.get("Preprocessing.temp.preprocess_functions"):
    del sys.modules["Preprocessing.temp.preprocess_functions"]

import pandas as pd
from Preprocessing.functions import *

# In[ ]:

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

# In[ ]:

df = pd.read_csv("Dataset/Raw/raw_data_TGDD_used.csv")
# Rename columns
rename_columns(df, inplace=True)
# Keep the first used laptop if there are many similar laptops
df = df.groupby("name", as_index=False).first()

# %%


df["name"] = df["name"].apply(lambda s: preprocess_name(s))
df["used_price"] = df["used_price"].apply(lambda s: preprocess_new_price(s))
df["new_price"] = df["new_price"].apply(lambda s: preprocess_new_price(s))

df['cpu_tech'] = df['cpu_tech'].apply(lambda s: preprocess_cpu(s))
df["ram_type"] = df["ram_type"].apply(lambda s: preprocess_ram_type(s))
df["ram_speed"] = df["ram_speed"].apply(lambda s: preprocess_ram_speed(s))
df["storage"] = df["storage"].apply(lambda s: preprocess_storage(s))
df["audio_tech"] = df["audio_tech"].apply(lambda s: preprocess_audio_tech(s))
df["resolution"] = df["resolution"].apply(lambda s: preprocess_resolution(s))
df["os"] = df["os"].apply(lambda s: preprocess_os(s))
df['graphics'] = df['graphics'].apply(lambda s: preprocess_gpu(s))
df['cpu_speed'] = df['cpu_speed'].apply(lambda s: preprocess_cpu_speed(s))
df['max_cpu_speed'] = df['max_cpu_speed'].apply(lambda s: preprocess_max_cpu_speed(s))
df['ram'] = df['ram'].apply(lambda s: preprocess_ram(s))
df['max_ram'] = df['max_ram'].apply(lambda s: preprocess_max_ram(s))
df['has_lightning'] = df['has_lightning'].apply(lambda s: preprocess_lightning(s))
df['material'] = df['material'].apply(lambda s: preprocess_material(s))
df['new_warranty'] = df['new_warranty'].apply(lambda s: preprocess_new_warranty(s))
df["used_warranty"] = df["used_warranty"].apply(lambda s: preprocess_used_warranty(s))
df["bluetooth_tech"] = df["wireless"].apply(lambda s: preprocess_wireless(s)[0])
df["wifi_tech"] = df["wireless"].apply(lambda s: preprocess_wireless(s)[1])
df["webcam"] = df["webcam"].apply(lambda s: preprocess_webcam(s))
df["battery"] = df["battery"].apply(lambda s: preprocess_battery(s))
df["weight"] = df["size_weight"].apply(lambda s: preprocessing_size_weight(s)[0])
df["thickness"] = df["size_weight"].apply(lambda s: preprocessing_size_weight(s)[1])
df["width"] = df["size_weight"].apply(lambda s: preprocessing_size_weight(s)[2])
df["length"] = df["size_weight"].apply(lambda s: preprocessing_size_weight(s)[3])
df['has_thundebolt'] = df['ports'].apply(lambda s: preprocess_thunderbolt(s))
df['has_antiglare'] = df['screen_tech'].apply(lambda s: preprocess_antiglare(s))

# %%
[size_weight, ports, screen_tech]

df.to_csv("tidydataset.csv", index=False)
