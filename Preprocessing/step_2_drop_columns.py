import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Preprocessing.utils import ordered_columns

# %%
df = pd.read_csv('Dataset/Tidy/1_dataset_renamed_preprocessed_dropped.csv')

# %%
# Tỉ lệ missing
labels = df.columns
na_values = df.isna().sum().values
not_na_values = df.shape[0] - df.isna().sum().values

width = 0.35  # the width of the bars: can also be len(x) sequence

fig, ax = plt.subplots(figsize=(15, 10))

ax.bar(labels, na_values, width, label='NA')
ax.bar(labels, not_na_values, width, bottom=na_values,
       label='Not NA')

ax.set_ylabel('Số lượng')
ax.set_title('Số lượng NA và Not NA')
ax.legend()

_ = plt.xticks(rotation=75)
plt.savefig('missing.png')
plt.show()
# %%

# Xuất file csv
missing_percentage = (100 * df.isna().sum() / df.shape[0])
missing_percentage.sort_values(ascending=False).to_csv('Preprocessing/1_1_missing_percentage.csv')
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

# Export
df = df[selected_columns_ordered]
df.to_csv('Dataset/Tidy/2_dataset_filtered_missing.csv', index=False)
