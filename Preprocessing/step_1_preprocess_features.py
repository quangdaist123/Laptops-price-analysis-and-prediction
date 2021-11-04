import pandas as pd
from Preprocessing.utils import *

# In[ ]:

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

# In[ ]:

df = pd.read_csv("Dataset/Raw/raw_data_TGDD_used.csv")
# Rename columns
df = rename_columns(df, alternative_name=alternative_names)
# Keep the first used laptop if there are many similar laptops
df = remove_duplicate_laptops(df)

# %%
# Preprocess features
df["brand"] = df["name"].apply(lambda s: preprocess_name(s))
df["used_price"] = df["used_price"].apply(lambda s: preprocess_used_price(s))
df["new_price"] = df["new_price"].apply(lambda s: preprocess_new_price(s))
df['cpu_type'] = df['cpu_type'].apply(lambda s: preprocess_cpu_type(s))
df['cached_cpu'] = df['cached_cpu'].apply(lambda s: preprocess_cached_cpu(s))
df["ram_type"] = df["ram_type"].apply(lambda s: preprocess_ram_type(s))
df["ram_speed"] = df["ram_speed"].apply(lambda s: preprocess_ram_speed(s))
df["storage"] = df["storage"].apply(lambda s: preprocess_storage(s))
df["audio_tech"] = df["audio_tech"].apply(lambda s: preprocess_audio_tech(s))
df["resolution"] = df["resolution"].apply(lambda s: preprocess_resolution(s))
df["os"] = df["os"].apply(lambda s: preprocess_os(s))
df['gpu_type'] = df['gpu_type'].apply(lambda s: preprocess_gpu_type(s))
df['cpu_speed'] = df['cpu_speed'].apply(lambda s: preprocess_cpu_speed(s))
df['max_cpu_speed'] = df['max_cpu_speed'].apply(lambda s: preprocess_max_cpu_speed(s))
df['ram'] = df['ram'].apply(lambda s: preprocess_ram(s))
df['max_ram'] = df['max_ram'].apply(lambda s: preprocess_max_ram(s))
df['has_lightning'] = df['has_lightning'].apply(lambda s: preprocess_has_lightning(s))
df['material'] = df['material'].apply(lambda s: preprocess_material(s))
df['new_warranty'] = df['new_warranty'].apply(lambda s: preprocess_new_warranty(s))
df["used_warranty"] = df["used_warranty"].apply(lambda s: preprocess_used_warranty(s))
df['has_thundebolt'] = df['ports'].apply(lambda s: preprocess_thunderbolt(s))
df['has_antiglare'] = df['screen_tech'].apply(lambda s: preprocess_antiglare(s))
df['has_touchscreen'] = df['has_touchscreen'].apply(lambda s: preprocess_has_touchscreen(s))
df['screen_size'] = df['screen_size'].apply(lambda s: preprocess_screen_size(s))
df['num_sd_slot'] = df['sd_slot'].apply(lambda s: preprocess_sd_slot(s))
df["webcam"] = df["webcam"].apply(lambda s: preprocess_webcam(s))
df["battery"] = df["battery"].apply(lambda s: preprocess_battery(s))

#### Tách thuộc tính wireless
df["bluetooth_tech"] = df["wireless"].apply(lambda s: preprocess_wireless(s)[0])
df["wifi_tech"] = df["wireless"].apply(lambda s: preprocess_wireless(s)[1])

#### Tách thuộc tính size_weight
df["weight"] = df["size_weight"].apply(lambda s: preprocessing_size_weight(s)[0])
df["thickness"] = df["size_weight"].apply(lambda s: preprocessing_size_weight(s)[1])
df["width"] = df["size_weight"].apply(lambda s: preprocessing_size_weight(s)[2])
df["length"] = df["size_weight"].apply(lambda s: preprocessing_size_weight(s)[3])

#### Tách thuộc tính savings
df['saved_percent'] = df['savings'].apply(lambda s: preprocess_savings(s)[0])
df['saved_money'] = df['savings'].apply(lambda s: preprocess_savings(s)[1])

#### Tách thuộc tính others
df['has_fingerprint'] = df['others'].apply(lambda s: preprocess_others(s)[0])
df['has_camera_lock'] = df['others'].apply(lambda s: preprocess_others(s)[1])
df['has_180_degree'] = df['others'].apply(lambda s: preprocess_others(s)[2])
df['has_face_id'] = df['others'].apply(lambda s: preprocess_others(s)[3])

# %%

# Drop unused columns
old_columns = ["name", "wireless", "size_weight", "ports", "screen_tech", "savings", "sd_slot", 'others']
df.drop(columns=old_columns, inplace=True)

# Reoder columns
df = df[ordered_columns]

# %%
df.to_csv("Dataset/Tidy/1_dataset_renamed_preprocessed_dropped.csv", index=False)
