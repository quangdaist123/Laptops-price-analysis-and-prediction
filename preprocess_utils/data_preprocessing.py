#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import preprocess_functions as pf


# In[ ]:


import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)


# In[ ]:


df = pd.read_csv('raw_combined_csv_ver2.csv')


# In[ ]:


df["Tên"] = df["Tên"].apply(lambda s: pf.preprocess_name(s))
df["Loại RAM"] = df["Loại RAM"].apply(lambda s: pf.preprocess_RAM(s))
df["Ổ cứng"] = df["Ổ cứng"].apply(lambda s: pf.preprocess_drive(s))
df["Hệ điều hành"] = df["Hệ điều hành"].apply(lambda s: pf.preprocess_os(s))
df["Camera"] = df["Camera"].apply(lambda s: pf.preprocess_camera(s))
df["Độ phân giải"] = df["Độ phân giải"].apply(lambda s: pf.preprocess_resolution(s))
df["Thông tin Pin"] = df["Thông tin Pin"].apply(lambda s: pf.preprocess_battery(s))
df["width"] = df["Kích thước"].apply(lambda s: pf.preprocessing_size(s)[0])
df["height"] = df["Kích thước"].apply(lambda s: pf.preprocessing_size(s)[1])
df["thickness"] = df["Kích thước"].apply(lambda s: pf.preprocessing_size(s)[2])
df['hasThunderbolt'] = df['Cổng giao tiếp'].apply(lambda s: pf.preprocess_thunderbolt(s))
df['hasAntiGlare'] = df['Công nghệ màn hình'].apply(lambda s: pf.preprocess_AntiGlare(s))
df['CPU'] = df['CPU'].apply(lambda s: pf.preprocess_cpu(s))
df['Card đồ họa'] = df['Card đồ họa'].apply(lambda s: pf.preprocess_gpu(s))
# df['RAM'] = np.array([*df.apply(lambda x: pf.preprocess_RAM_tiki(x), axis=1).to_list()])[:, 0]
# df['Loại RAM'] = np.array([*df.apply(lambda x: pf.preprocess_RAM_tiki(x), axis=1).to_list()])[:, 1]
# df['Tốc độ Bus RAM'] = np.array([*df.apply(lambda x: pf.preprocess_RAM_tiki(x), axis=1).to_list()])[:, 2]
df['RAM'], df['Loại RAM'], df['Tốc độ Bus RAM'] = np.hsplit(np.array([*df.apply(lambda x: pf.preprocess_RAM_tiki(x), axis=1).to_list()]),3)


# In[ ]:


df.to_csv('data.csv')

