import pandas as pd
import numpy as np

from Preprocessing.utils.utils_step_1 import ordered_columns

# %%
df = pd.read_csv('Dataset/Tidy/1_dataset_renamed_preprocessed_dropped.csv')

# %% Column
# Tỉ lệ missing
labels = df.columns
na_values = df.isna().sum().values
not_na_values = df.shape[0] - df.isna().sum().values

# width = 0.35  # the width of the bars: can also be len(x) sequence
# fig, ax = plt.subplots(figsize=(15, 10))
#
# ax.bar(labels, na_values, width, label='NA')
# ax.bar(labels, not_na_values, width, bottom=na_values,
#        label='Not NA')
#
# ax.set_ylabel('Số lượng')
# ax.set_title('Số lượng NA và Not NA')
# ax.legend()
#
# _ = plt.xticks(rotation=75)
# plt.savefig('missing.png')
# plt.show()
# %%

# Xuất file csv
missing_percentage = (100 * df.isna().sum() / df.shape[0])
missing_percentage.sort_values(ascending=False).to_csv('Preprocessing/utils/1_1_missing_percentage.csv')
# %%
# Loại bỏ những cột có tỉ lệ missing values trên 35%
missing_percentage = missing_percentage.apply(lambda percent: True if percent < 35 else np.nan)
non_missing = missing_percentage.dropna()
selected_columns = list(non_missing.index)

# Sắp xếp lại thứ tự các cột
selected_columns_ordered = []
for column in ordered_columns:
    if column in selected_columns:
        selected_columns_ordered.append(column)

df = df[selected_columns_ordered]


# %% Row

def fill_missing(row_index, column_name, value):
    df.iloc[row_index - 2, df.columns.get_loc(column_name)] = value
    print(f'Đã điền cho lap ở dòng thứ {row_index} trong file EXCEL')


# %%

# Acer Swift 1 SF114 32 P2SG N5000/4GB/64GB/Win10 (NX.GZJSV.001)
fill_missing(34, 'storage', 128)

# Dell Inspiron 15 5584 i5 8265U/8GB/2TB/2GB MX130/Win10 (N5I5353W)
fill_missing(154, 'storage', 'HDD 1 TB')

# Dell Inspiron 5480 i5 8265U/8GB/256GB/2GB MX150/Office365/Win10 (X6C892)
fill_missing(157, 'released', 2018)

# Lenovo Legion Y530 15 i7 8750H/8GB/2TB+16GB/4GB GTX1050Ti/Win10 (81FV008LVN)
fill_missing(269, 'storage', 'HDD 1 TB')
# fill_missing(269,'webcam','')

# MacBook Pro Touch 16 inch 2019 i7 2.6GHz/16GB/512GB/4GB Radeon Pro 5300M (MVVJ2SA/A)
fill_missing(302, 'gpu_type', 'Radeon')
fill_missing(202, 'ram', 16)

# Apple Macbook Air 2015 MJVE2ZP/A i5 5250U/4GB/128GB
fill_missing(66, 'cpu_type', 'i5')
fill_missing(66, 'storage', 128)
fill_missing(66, 'os', 'MacOS')
fill_missing(66, 'released', '2015')

# Apple Macbook Air MMGF2ZP/A i5 1.6GHz/8GB/128GB (2015)
fill_missing(69, 'released', 2015)

# Apple Macbook Pro 2019 Touch i7 2.6GHz/16GB/256GB/ Radeon 555X (MV902SA/A)
fill_missing(70, 'gpu_type', 'i7')
fill_missing(70, 'released', 2019)

# Apple Macbook Pro MPXQ2SA/A i5 2.3GHz/8GB/128GB (2017)
fill_missing(71, 'released', 2017)

# Apple Macbook Pro Touch MLH12SA/A i5 6267U/8GB/256GB (2016)
fill_missing(72, 'released', 2016)

# Apple Macbook Pro Touch MPXV2SA/A i5 3.1GHz/8GB/256GB (2017)
fill_missing(73, 'released', 2017)

# %% Export
df.to_csv('Dataset/Tidy/2_dataset_missings_filtered.csv', index=False)
