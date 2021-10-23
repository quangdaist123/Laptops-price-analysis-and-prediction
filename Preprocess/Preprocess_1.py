import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import f_oneway
from math import ceil

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

# %%
df = pd.read_csv("Raw dataset/raw_combined_csv_ver2.csv")


# %%

def preprocess_name(name):
    filters = ["laptop", "laptop gaming"]
    brand_name = np.nan
    if name is not None:
        name_lowercased = name.lower()
        # Bỏ chữ "Laptop" và "Laptop gaming"
        for filter in filters:
            if name_lowercased[:len(filter)] == filter:
                removed_laptop_word = name[len(filter):]
                brand_name = removed_laptop_word.split()[0]
        # Gom "Microsoft Surface... " và "Surface..." => "Microsoft"
        if "surface" in name_lowercased:
            brand_name = "Microsoft"
        # "Vivobook... " => "Asus"
        if "vivobook" in name_lowercased:
            brand_name = "Asus"
        # Trừ "HP", "MSI", "LG", Chỉ có chữ đầu tiên của các tên hãng đều được in hoa
        if str(brand_name) != "nan" and brand_name not in ["HP", "MSI", "LG"]:
            brand_name = brand_name.capitalize()

    return brand_name


def filter_non_laptops(df):
    df = df.copy()
    freq = dict(df["brand"].value_counts())
    new_column = []
    for i, row in df.iterrows():
        if str(row["brand"]) != "nan" and freq[row["brand"]] == 1:
            new_column.append(np.nan)
        else:
            new_column.append(row["brand"])
    df["brand"] = new_column
    df.dropna(subset=['brand'], inplace=True)
    return df


# %%
# THUẬNNNNNN
df["brand"] = df["Tên"].apply(lambda s: preprocess_name(s))
df["ram"] = df["Loại RAM"].apply(lambda s: preprocess_RAM(s))
df["drive"] = df["Ổ cứng"].apply(lambda s: preprocess_drive(s))


new_column = []
for i, row in df.iterrows():
    new_column.append(preprocess_name(row["Tên"]))
df = filter_non_laptops(df)
df["brand"].value_counts()


# %% Loại RAM

def preprocess_RAM(ram):
    types_of_RAM = ["LPDDR4X", "DDR4"]
    ram_new = np.nan
    if ram is not None and str(ram) != "nan":
        ram_upercased = ram.upper()
        for type in types_of_RAM:
            if type in ram_upercased:
                ram_new = type
                break
    return ram_new


new_column = []
for i, row in df.iterrows():
    print(i, preprocess_RAM(row["Loại RAM"]))

# %%
new_column = []
for i, row in df.iterrows():
    new_column.append(preprocess_RAM(row["Loại RAM"]))
df["Loại RAM"] = new_column
df["Loại RAM"].value_counts()


# %% Ổ cứng

def preprocess_drive(drive):
    common_drive_capacity = ["128GB", "256GB", "512GB", "1TB"]
    new_drive = np.nan
    if drive is not None and str(drive) != "nan":
        drive_tight_uppercased = drive.replace(" ", "").upper()
        for capacity in common_drive_capacity:
            if capacity in drive_tight_uppercased:
                new_drive = capacity
                break
    return new_drive


# %%
new_column = []
for i, row in df.iterrows():
    new_column.append(preprocess_drive(row["Ổ cứng"]))

df["Ổ cứng"] = new_column
df["Ổ cứng"].value_counts()

# %%
