import pandas as pd
from Preprocessing.utils.utils_step_1 import *

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)


df = pd.read_csv("Dataset/Raw/raw_data_TGDD_used.csv")
# Rename columns
df = rename_columns(df, alternative_name=alternative_names)
# Keep the first used laptop if there are many similar laptops
df = remove_duplicate_laptops(df)

# %%
# Preprocess features
df["brand"] = df["name"].apply(preprocess_name)
df["used_price"] = df["used_price"].apply(preprocess_used_price)
df["new_price"] = df["new_price"].apply(preprocess_new_price)
df['cpu_type'] = df['cpu_type'].apply(preprocess_cpu_type)
df['cached_cpu'] = df['cached_cpu'].apply(preprocess_cached_cpu)
df["ram_type"] = df["ram_type"].apply(preprocess_ram_type)
df["ram_speed"] = df["ram_speed"].apply(preprocess_ram_speed)
df["storage"] = df["storage"].apply(preprocess_storage)
df["audio_tech"] = df["audio_tech"].apply(preprocess_audio_tech)
df["resolution"] = df["resolution"].apply(preprocess_resolution)
df["os"] = df["os"].apply(preprocess_os)
df['gpu_type'] = df['gpu_type'].apply(preprocess_gpu_type)
df['cpu_speed'] = df['cpu_speed'].apply(preprocess_cpu_speed)
df['max_cpu_speed'] = df['max_cpu_speed'].apply(preprocess_max_cpu_speed)
df['ram'] = df['ram'].apply(preprocess_ram)
df['max_ram'] = df['max_ram'].apply(preprocess_max_ram)
df['has_lightning'] = df['has_lightning'].apply(preprocess_has_lightning)
df['material'] = df['material'].apply(preprocess_material)
df['new_warranty'] = df['new_warranty'].apply(preprocess_new_warranty)
df["used_warranty"] = df["used_warranty"].apply(preprocess_used_warranty)
df['has_thundebolt'] = df['ports'].apply(preprocess_thunderbolt)
df['has_antiglare'] = df['screen_tech'].apply(preprocess_antiglare)
df['has_touchscreen'] = df['has_touchscreen'].apply(preprocess_has_touchscreen)
df['screen_size'] = df['screen_size'].apply(preprocess_screen_size)
df["webcam"] = df["webcam"].apply(preprocess_webcam)
df["battery"] = df["battery"].apply(preprocess_battery)
df['num_sd_slot'] = df['sd_slot'].apply(preprocess_sd_slot)
df['scan_frequency'] = df['scan_frequency'].apply(preprocess_scan_frequency)

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
