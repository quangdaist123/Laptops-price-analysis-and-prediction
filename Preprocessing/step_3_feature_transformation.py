import numpy as np
import pandas as pd
import math
import re

from Preprocessing.utils.utils_step_1 import correct_dtypes

# %%
df = pd.read_csv('Dataset/Tidy/2_dataset_missings_filtered.csv')
df = correct_dtypes(df)


# %%

def make_ppi(row):
    """
    Tạo thuộc tính PPI từ thuộc tính 'resolution' và 'screen_size'
    """
    length_width = re.findall("\\d*\\.?,?\\d+", row['resolution'])

    PPI = math.sqrt(pow(int(length_width[0]), 2) + pow(int(length_width[1]), 2)) / row['screen_size']

    # Mỗi 'row' là một hàng trong dataframe nên mình sẽ sử dụng 2 thuộc tính của nó
    if str(row['resolution']) == "nan" or str(row['screen_size']) == "nan":
        return np.nan
    else:
        return PPI
    # return chỉ số PPI


# %%
# Kiểm tra cho một hàng bất kì trong df
random_row = df.iloc[99, :]
print(make_ppi(random_row))

# %%
# Kiểm tra cho toàn dataframe
df['ppi'] = df.apply(lambda s: make_ppi(s), axis=1)
df['ppi'].value_counts()

# %% Export
df.to_csv('Dataset/Tidy/3_dataset_feature_added.csv', index=False)
