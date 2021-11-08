# brand               object
# cpu_type            object
# cpu_speed          float64 -> Chuyển về biến phân loại -> object
# max_cpu_speed      float64 -> Chuyển về biến phân loại -> object
# gpu_type            object
# ram_type            object
# ram                float64 -> Chuyển về biến phân loại -> object
# ram_speed          float64 -> Chuyển về biến phân loại -> object
# storage            float64 -> Chuyển về biến phân loại -> object
# screen_size        float64 -> Chuyển về biến phân loại -> object
# resolution          object
# webcam              object
# num_sd_slot          int64 -> Chuyển về biến phân loại -> object
# material            object
# os                  object
# audio_tech          object
# bluetooth_tech     float64 -> Chuyển về biến phân loại -> object
# wifi_tech           object
# weight             float64
# thickness          float64
# width              float64
# length             float64
# released           float64 -> Chuyển về biến phân loại -> object
# has_lightning      float64 -> Chuyển về biến phân loại -> object
# has_thundebolt       int64 -> Chuyển về biến phân loại -> object
# has_touchscreen      int64 -> Chuyển về biến phân loại -> object
# has_fingerprint      int64 -> Chuyển về biến phân loại -> object
# has_camera_lock      int64 -> Chuyển về biến phân loại -> object
# has_180_degree       int64 -> Chuyển về biến phân loại -> object
# has_face_id          int64 -> Chuyển về biến phân loại -> object
# has_antiglare        int64 -> Chuyển về biến phân loại -> object
# new_warranty         int64 -> Chuyển về biến phân loại -> object
# used_warranty      float64 -> Chuyển về biến phân loại -> object
# used_price           int64

import pandas as pd
import numpy as np

df = pd.read_csv('./Dataset/Tidy/2_dataset_filtered_missing.csv')
# %%

df['cpu_speed'] = df['cpu_speed'].astype('object')
df['max_cpu_speed'] = df['max_cpu_speed'].astype('object')
df['ram'] = df['ram'].astype('object')
df['ram_speed'] = df['ram_speed'].astype('object')
df['storage'] = df['storage'].astype('object')
df['screen_size'] = df['screen_size'].astype('object')
df['num_sd_slot'] = df['num_sd_slot'].astype('object')
df['bluetooth_tech'] = df['bluetooth_tech'].astype('object')
df['released'] = df['released'].astype('object')
df['has_lightning'] = df['has_lightning'].astype('object')
df['has_thundebolt'] = df['has_thundebolt'].astype('object')
df['has_touchscreen'] = df['has_touchscreen'].astype('object')
df['has_fingerprint'] = df['has_fingerprint'].astype('object')
df['has_camera_lock'] = df['has_camera_lock'].astype('object')
df['has_180_degree'] = df['has_180_degree'].astype('object')
df['has_face_id'] = df['has_face_id'].astype('object')
df['has_antiglare'] = df['has_antiglare'].astype('object')
df['new_warranty'] = df['new_warranty'].astype('object')
df['used_warranty'] = df['used_warranty'].astype('object')

# %% Chuyển các giá trị np.nan trong các cột object
# thành 'None' để đồng nhất kiểu dữ liệu

for column in df.select_dtypes(include=['object']).columns:
    df[column] = df[column].replace(np.nan, 'None')

df.to_csv('Dataset/Tidy/3_dataset_dtypes_corrected.csv', index=False)
