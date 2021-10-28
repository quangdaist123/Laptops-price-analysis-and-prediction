import pandas as pd
from os import listdir
from os.path import isfile, join

FOLDER_PATH = "Dataset/Raw"
onlyfiles = [f for f in listdir(FOLDER_PATH) if isfile(join("Dataset/Raw", f)) and ".py" not in f]

#%%
for filename in onlyfiles:
    df = pd.read_csv("Dataset/Raw/" + filename)
    print("Dataset: ", filename)
    print("Số dòng: ", len(df))
    print("Số cột: ", len(df.columns))